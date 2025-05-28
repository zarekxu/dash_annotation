def _parse_losses(self, losses):
    """Parse the raw outputs (losses) and synchronize log_vars across GPUs.
    
    Automatically detects and resolves key mismatches by broadcasting from
    the GPU with the most complete set of keys.
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

    # Step 2: Validate key consistency across GPUs
    if dist.is_available() and dist.is_initialized():
        rank = dist.get_rank()
        world_size = dist.get_world_size()

        # Encode local keys
        local_keys = list(log_vars.keys())
        local_key_str = ','.join(local_keys)
        key_bytes = local_key_str.encode('utf-8')
        max_len = 1024
        key_tensor = torch.zeros(max_len, dtype=torch.uint8, device=loss.device)
        key_tensor[:len(key_bytes)] = torch.tensor(list(key_bytes), dtype=torch.uint8, device=loss.device)

        # Gather key sets from all ranks
        gathered_key_tensors = [torch.zeros_like(key_tensor) for _ in range(world_size)]
        dist.all_gather(gathered_key_tensors, key_tensor)

        # Decode gathered keys
        gathered_keys = []
        for t in gathered_key_tensors:
            k_str = bytes(t.cpu().numpy()).decode('utf-8').rstrip('\x00')
            gathered_keys.append(set(k_str.split(',')) if k_str else set())

        # Find rank with max key count
        key_lengths = [len(kset) for kset in gathered_keys]
        source_rank = key_lengths.index(max(key_lengths))
        full_key_set = gathered_keys[source_rank]

        if any(kset != full_key_set for kset in gathered_keys):
            if rank == 0:
                print(f"[Warning] Inconsistent log_vars keys detected. Broadcasting from rank {source_rank}.")

            # Step 3: Broadcast full log_vars from source_rank
            if rank == source_rank:
                obj_to_broadcast = {k: v.detach().cpu().item() for k, v in log_vars.items()}
            else:
                obj_to_broadcast = {}

            obj_list = [obj_to_broadcast]
            dist.broadcast_object_list(obj_list, src=source_rank)

            # Overwrite log_vars with broadcasted copy
            log_vars = OrderedDict(
                (k, torch.tensor(v, device=loss.device)) for k, v in obj_list[0].items()
            )

        # Step 4: Reduce all values across GPUs
        for k, v in log_vars.items():
            val = v if isinstance(v, torch.Tensor) else torch.tensor(v, device=loss.device)
            dist.all_reduce(val)
            log_vars[k] = val.div_(world_size).item()

    log_vars['loss'] = loss.item() if isinstance(loss, torch.Tensor) else loss
    return loss, log_vars
