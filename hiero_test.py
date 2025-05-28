def _parse_losses(self, losses):
    log_vars = OrderedDict()

    for loss_name, loss_value in losses.items():
        if isinstance(loss_value, torch.Tensor):
            log_vars[loss_name] = loss_value.mean()
        elif isinstance(loss_value, list):
            log_vars[loss_name] = sum(_loss.mean() for _loss in loss_value)
        else:
            raise TypeError(f'{loss_name} is not a tensor or list of tensors')

    loss = sum(_value for _key, _value in log_vars.items() if 'loss' in _key)

    # === Fast validation: copy log_vars from GPU 0 to GPU 1 ===
    if dist.is_available() and dist.is_initialized():
        rank = dist.get_rank()

        # Convert log_vars to a CPU object
        if rank == 0:
            obj_to_broadcast = {k: v.detach().cpu().item() for k, v in log_vars.items()}
        else:
            obj_to_broadcast = {}

        # Prepare object list for broadcasting
        obj_list = [obj_to_broadcast]

        # Only broadcast from rank 0 to rank 1
        if rank in [0, 1]:
            dist.broadcast_object_list(obj_list, src=0)

            # GPU 1 will override its local log_vars
            if rank == 1:
                log_vars = OrderedDict((k, torch.tensor(v, device=loss.device)) for k, v in obj_list[0].items())

        # Reduce all values
        for loss_name, loss_value in log_vars.items():
            dist.all_reduce(loss_value.div_(dist.get_world_size()))
            log_vars[loss_name] = loss_value.item()

    log_vars['loss'] = loss.item() if isinstance(loss, torch.Tensor) else loss
    return loss, log_vars
