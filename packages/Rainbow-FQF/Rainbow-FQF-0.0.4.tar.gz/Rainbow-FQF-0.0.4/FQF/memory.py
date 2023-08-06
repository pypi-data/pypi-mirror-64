import torch
import random
import numpy as np

"""
code reference
https://github.com/rlcode/per/
Thanks RLCode! 
"""
class PER:  # stored as ( s, a, r, s_ ) in SumTree

    def __init__(
            self,
            capacity:int, batch_size:int,
            epsilon:float, alpha:float,
            beta:float, beta_inc:float,
            device:torch.device):
        self.tree = SumTree(capacity)
        self.capacity = capacity
        self.batch_size = batch_size
        self.e = epsilon
        self.a = alpha
        self.beta = beta
        self.beta_increment_per_sampling = beta_inc
        self.device = device

    def _get_priority(self, error):
        return (np.abs(error) + self.e) ** self.a

    def add(self, sample):
        p = np.max(self.tree.tree) + self.e
        self.tree.add(p, sample)

    def sample(self):
        batch = []
        idxs = []
        segment = self.tree.total() / self.batch_size
        priorities = []

        self.beta = np.min([1., self.beta + self.beta_increment_per_sampling])

        for i in range(self.batch_size):
            a = segment * i
            b = segment * (i + 1)

            s = random.uniform(a, b)
            (idx, p, data) = self.tree.get(s)
            priorities.append(p)
            batch.append(data)
            idxs.append(idx)

        sampling_probabilities = priorities / self.tree.total()
        is_weight = np.power(self.tree.n_entries * sampling_probabilities, -self.beta)
        is_weight /= is_weight.max()

        return self.split_batch(batch), idxs, is_weight

    def split_batch(self, batch):
        batch = np.transpose(batch)
        state_transf = \
            lambda x: torch.tensor(np.vstack(x), dtype=torch.float32).to(self.device)
        other_transf = \
            lambda x: torch.tensor(x.astype(np.float32), dtype=torch.float32).to(self.device)
        s, ns = state_transf(batch[0]), state_transf(batch[3])
        a, r, d = other_transf(batch[1]), other_transf(batch[2]), other_transf(batch[4])
        return s, a, r, ns, d

    def update(self, idxs, errors):
        for idx, error in zip(idxs, errors):
            p = self._get_priority(error)
            self.tree.update(idx, p)

class SumTree:
    write = 0

    def __init__(self, capacity):
        self.capacity = capacity
        self.tree = np.zeros(2 * capacity - 1)
        self.data = np.zeros(capacity, dtype=object)
        self.n_entries = 0

    # update to the root node
    def _propagate(self, idx, change):
        parent = (idx - 1) // 2

        self.tree[parent] += change

        if parent != 0:
            self._propagate(parent, change)

    # find sample on leaf node
    def _retrieve(self, idx, s):
        left = 2 * idx + 1
        right = left + 1

        if left >= len(self.tree):
            return idx

        if s <= self.tree[left]:
            return self._retrieve(left, s)
        else:
            return self._retrieve(right, s - self.tree[left])

    def total(self):
        return self.tree[0]

    # store priority and sample
    def add(self, p, data):
        idx = self.write + self.capacity - 1

        self.data[self.write] = data
        self.update(idx, p)

        self.write += 1
        if self.write >= self.capacity:
            self.write = 0

        if self.n_entries < self.capacity:
            self.n_entries += 1

    # update priority
    def update(self, idx, p):
        change = p - self.tree[idx]

        self.tree[idx] = p
        self._propagate(idx, change)

    # get priority and sample
    def get(self, s):
        idx = self._retrieve(0, s)
        dataIdx = idx - self.capacity + 1

        return (idx, self.tree[idx], self.data[dataIdx])