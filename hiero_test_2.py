def _parse_losses(self, losses):
    """Parse the raw outputs (losses) of the network and sync across GPUs.

    If the keys in `log_vars` are inconsistent across ranks, automatically
    broadcast the correct version from rank 0 to all ranks.

    Returns:
        tuple[Tensor, dict]: (loss, log_vars)
    """
    from collections import OrderedDict
    import torch.distributed as dist

    log_vars = OrderedDict()

    # Step 1: Aggregate local losses
    for loss_name, loss_value in losses.items():
        if isinstance(loss_value, torch.Tensor):
            log_vars[loss_name] = loss_value.mean()
        elif isinstance(loss_value, list):
            log_vars[loss_name] = sum(_loss.mean() for _loss in loss_value)
        else:
            raise TypeError(f'{loss_name} is not a tensor or list of tensors')

    loss = sum(v for k, v in log_vars.items() if 'loss' in k)

    # Step 2: Attempt to validate key consistency across ranks
    if dist.is_available() and dist.is_initialized():
        rank = dist.get_rank()
        world_size = dist.get_world_size()

        # Encode keys into a string
        local_keys_str = ','.join(log_vars.keys())
        local_key_bytes = local_keys_str.encode('utf-8')
        max_len = 1024  # max allowed key string length

        key_tensor = torch.zeros(max_len, dtype=torch.uint8, device=loss.device)
        key_tensor[:len(local_key_bytes)] = torch.tensor(list(local_key_bytes), dtype=torch.uint8, device=loss.device)

        # Gather key strings from all ranks
        gathered_keys = [torch.zeros_like(key_tensor) for _ in range(world_size)]
        dist.all_gather(gathered_keys, key_tensor)

        # Decode all gathered key sets
        gathered_key_sets = []
        for t in gathered_keys:
            k_str = bytes(t.cpu().numpy()).decode('utf-8').rstrip('\x00')
            gathered_key_sets.append(set(k_str.split(',')))

        # Check if all key sets are identical
        all_same = all(gathered_key_sets[0] == kset for kset in gathered_key_sets)

        if not all_same:
            if rank == 0:
                print('[Warning] log_vars keys are inconsistent across GPUs. Broadcasting from rank 0.')

            # Step 3: Prepare full log_vars on rank 0 to broadcast
            if rank == 0:
                obj_to_broadcast = {k: v.detach().cpu().item() for k, v in log_vars.items()}
            else:
                obj_to_broadcast = {}

            obj_list = [obj_to_broadcast]
            dist.broadcast_object_list(obj_list, src=0)

            # Step 4: Overwrite log_vars with the one from rank 0
            log_vars = OrderedDict(
                (k, torch.tensor(v, device=loss.device)) for k, v in obj_list[0].items()
            )

        # Step 5: Reduce all log_vars across GPUs
        for k in log_vars:
            val = log_vars[k]
            if not isinstance(val, torch.Tensor):
                val = torch.tensor(val, device=loss.device)
            dist.all_reduce(val)
            log_vars[k] = val.div_(world_size).item()

    log_vars['loss'] = loss.item() if isinstance(loss, torch.Tensor) else loss
    return loss, log_vars
