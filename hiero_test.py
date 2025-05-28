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
    
        if rank == 0:
            obj_to_broadcast = {k: v.detach().cpu().item() for k, v in log_vars.items()}
        else:
            obj_to_broadcast = {}
    
        obj_list = [obj_to_broadcast]
    
        # All ranks participate
        dist.broadcast_object_list(obj_list, src=0)
    
        # Non-rank-0 overwrites their log_vars with the broadcasted copy
        if rank != 0:
            log_vars = OrderedDict((k, torch.tensor(v, device=loss.device)) for k, v in obj_list[0].items())
    
        # Reduce loss values across all ranks
        for loss_name, loss_value in log_vars.items():
            val_tensor = torch.tensor(loss_value, device=loss.device) if not isinstance(loss_value, torch.Tensor) else loss_value
            dist.all_reduce(val_tensor.div_(dist.get_world_size()))
            log_vars[loss_name] = val_tensor.item()


    log_vars['loss'] = loss.item() if isinstance(loss, torch.Tensor) else loss
    return loss, log_vars
