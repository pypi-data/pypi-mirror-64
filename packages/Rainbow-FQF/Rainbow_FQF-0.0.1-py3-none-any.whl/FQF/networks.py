import os
import torch
import torch.nn as nn
import FQF.utils as fqfutils

class FQFNetworks(nn.Module):
    def __init__(self, save_path_and_name="./save_model/FQF.pth"):
        super().__init__()
        self.save_path_and_name = save_path_and_name

    def save(self):
        if not os.path.exists(self.save_path_and_name):
            fqfutils.mkdirs_only_path(self.save_path_and_name)
        torch.save(self.state_dict(), self.save_path_and_name)

    def load(self):
        if os.path.exists(self.save_path_and_name):
            self.load_state_dict(torch.load(self.save_path_and_name))


class LinearNet(FQFNetworks):
    def __init__(self, state_size, hidden_size, n_actions, n_supports, **kwargs):
        super(LinearNet, self).__init__(**kwargs)
        self.n_actions, self.n_supports = n_actions, n_supports
        self.fc1 = nn.Linear(state_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.support = nn.Linear(hidden_size, n_actions * n_supports)
        self.quantile = nn.Linear(hidden_size, n_supports)

    def forward_hidden(self, state) -> torch.Tensor:
        x = torch.relu(self.fc1(state))
        x = torch.relu(self.fc2(x))
        return x

    def _forward_support(self, x) -> torch.Tensor:
        support = self.support(x)\
            .reshape(x.shape[0], self.n_actions, self.n_supports)
        return support

    def _forward_quantile(self, x) -> torch.Tensor:
        x = self.quantile(x)
        pdf = torch.softmax(x, dim=1)
        cdf = torch.cumsum(pdf, dim=1)
        cdf_midval = fqfutils.get_midval(cdf)
        cdf_midval = cdf_midval\
            .reshape(x.shape[0], 1, self.n_supports)
        return cdf_midval

    def forward_support(self, state) -> torch.Tensor:
        x = self.forward_hidden(state)
        support = self._forward_support(x)
        return support

    def forward(self, state) -> (torch.Tensor, torch.Tensor):
        x = self.forward_hidden(state)
        support = self._forward_support(x)
        quantile = self._forward_quantile(x)
        return support, quantile

