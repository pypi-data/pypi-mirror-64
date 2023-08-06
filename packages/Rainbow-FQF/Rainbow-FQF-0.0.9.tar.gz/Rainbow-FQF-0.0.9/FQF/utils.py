from functools import reduce
from torch.nn import Module
import torch
import os

def mkdirs_only_path(path_and_name:str) -> None:
    reversed_pan = list(reversed(path_and_name))
    path = list(reversed(reversed_pan[reversed_pan.index("/"):]))
    path_str = reduce(lambda x, y : x + y, path)
    os.makedirs(path_str)

def get_midval(x:torch.Tensor, device) -> torch.Tensor:
    x_ = x[:, :-1]
    x_ = torch.cat((torch.zeros(x.shape[0], 1).to(device), x_), dim=1)
    stacked = torch.stack((x, x_.detach()), dim=2)
    midvals = stacked.mean(dim=2)
    return midvals

def hard_target_update(main_net:Module, target_net:Module) -> None:
    target_net.load_state_dict(main_net.state_dict())

def soft_target_update(main_net:Module, target_net:Module, tau:float=1e-1):
    params = zip(target_net.parameters(), main_net.parameters())
    for target_param, local_param in params:
        target_param.data.copy_(tau * local_param.data + (1.0 - tau) * target_param.data)

def gather_support(supports:torch.Tensor, actions:torch.Tensor) -> torch.Tensor:
    n_sup = supports.shape[-1]
    n_bat = supports.shape[0]
    indices = actions.repeat(n_sup).reshape(n_bat, 1, n_sup).long()
    return supports.gather(1, indices).squeeze()

def preprocess_state(state, device):
    return torch.tensor(state, dtype=torch.float32).unsqueeze(0).to(device)

if __name__ == '__main__':
    x = torch.arange(1, 101).reshape(10, 10).float()
    print (get_midval(x))



