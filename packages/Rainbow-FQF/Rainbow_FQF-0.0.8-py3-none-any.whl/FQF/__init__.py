import gym
import torch
import torch.nn.functional as F
import torch.optim as optim
import FQF.utils as utils
import FQF.networks as networks
import FQF.memory as memory
from torch.nn import Module
from torch.utils.tensorboard.writer import SummaryWriter


class FQF:
    def __init__(
            self, env: gym.Env,
            state_size: int = 4, hidden_size: int = 256,
            n_actions: int = 2, n_supports: int = 32,
            memory_capacity: int = 50000, batch_size: int = 32,
            memory_eps: float = 0.01, memory_alp: float = 0.4,
            memory_bet: float = 0.6, memory_beta_inc: float = 0.01,
            gamma=0.98, epsilon=1, epsilon_decay=0.99995, epsilon_min=0.05,
            soft_update_tau: float = 0.1, lr: float = 1e-6,
            total_episode: int = 30000, save_path="/content/gdrive/My Drive/FQF/model.pth",
            *args, **kwargs):
        # init env
        self.env = env
        # init device
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        # init parameters
        self.state_size, self.hidden_size = state_size, hidden_size
        self.n_actions, self.n_supports = n_actions, n_supports
        self.soft_update_tau = soft_update_tau
        self.gamma = gamma
        # init networks
        self.save_path = save_path
        self.main_net, self.target_net = self._init_network()
        # init optim
        self.optimizer = optim.Adam(self.main_net.parameters(), lr)
        # init memory
        self.memory = memory.PER(
            memory_capacity, batch_size, memory_eps,
            memory_alp, memory_bet, memory_beta_inc,
            self.device
        )
        # exploration
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        # steps
        self.total_episode = total_episode
        self.current_episode = 0
        self.current_step = 0
        # log
        self.writer = SummaryWriter()

    def _init_network(self) -> (Module, Module):
        main_net = networks.LinearNet(
            self.state_size, self.hidden_size, self.n_actions, self.n_supports,
            save_path_and_name=self.save_path).to(self.device)
        main_net.load()
        target_net = networks.LinearNet(
            self.state_size, self.hidden_size, self.n_actions, self.n_supports,
            save_path_and_name=self.save_path).to(self.device)
        utils.hard_target_update(main_net, target_net)
        return main_net, target_net

    def init_network(self) -> None:
        self.main_net, self.target_net = self._init_network()

    def soft_target_update(self) -> None:
        utils.soft_target_update(
            self.main_net, self.target_net, self.soft_update_tau)
        return None

    def get_action_greedy(self, state: torch.Tensor) -> (torch.Tensor, torch.Tensor):
        support, tau = self.main_net.forward(state)
        q_value_distribution = torch.mul(support, tau)
        q_value = torch.sum(q_value_distribution, dim=2)
        action = torch.argmax(q_value, dim=1)
        return action, q_value, support

    def get_action(self, state: torch.Tensor) -> int:
        action, q_value, support = self.get_action_greedy(state)
        if torch.rand(1).item() <= self.epsilon:
            action = torch.randint(low=0, high=self.n_actions, size=(1,))
        self.writer.add_scalar(
            "q_value/action", q_value[0, action].item(), self.current_step)
        self.writer.add_scalar(
            "q_value/max", q_value.max().item(), self.current_step)
        self.writer.add_scalar(
            "q_value/avg", q_value.mean().item(), self.current_step)
        self.writer.add_histogram(
            "value_dist", support.squeeze()[action].cpu().detach().numpy(),
            self.current_step
        )
        return action.item()

    def train(self):
        (s, a, r, ns, d), mem_idx, _ = self.memory.sample()
        # get support, next support, tau, next tau
        sup, tau = self.main_net.forward(s)
        n_sup, n_tau = self.target_net.forward(ns)
        na, _, _ = self.get_action_greedy(ns)
        # gather supports
        sup, n_sup = \
            utils.gather_support(sup, a), utils.gather_support(n_sup, na)
        # get delta
        td_target = r.unsqueeze(1) + (1 - d).unsqueeze(1) * self.gamma * n_sup
        delta = td_target - sup
        delta_mask = (delta < 0).float()
        # get loss
        loss = F.smooth_l1_loss(sup, td_target.detach(), reduction="none")
        loss = loss * torch.abs(tau.squeeze() - delta_mask)
        self.memory.update(
            mem_idx, torch.abs(torch.sum(loss, dim=1)).cpu().detach().numpy())
        # train
        self.optimizer.zero_grad()
        loss = loss.mean()
        loss.backward()
        self.optimizer.step()
        # write log
        self.writer.add_scalar("loss", loss.item(), self.current_step)
        self.soft_target_update()

    def write_net_hist(self):
        self.writer.add_histogram(
            "fc/fc1", self.main_net.fc1.weight.cpu().detach().numpy(), int(self.current_episode/100))
        self.writer.add_histogram(
            "fc/fc2", self.main_net.fc2.weight.cpu().detach().numpy(), int(self.current_episode/100))
        self.writer.add_histogram(
            "fc/supports", self.main_net.support.weight.cpu().detach().numpy(),
            int(self.current_episode/100))
        self.writer.add_histogram(
            "fc/quantiles", self.main_net.quantile.weight.cpu().detach().numpy(),
            int(self.current_episode/100))

    def timestep(self, state):
        state_inp = utils.preprocess_state(state, self.device)
        action = self.get_action(state_inp)
        next_state, reward, done, _ = self.env.step(action)
        self.memory.add((state, action, reward / 100, next_state, done))
        self.train()
        self.epsilon = max(self.epsilon * self.epsilon_decay, self.epsilon_min)
        self.writer.add_scalar("epsilon", self.epsilon, self.current_step)
        self.writer.add_scalar("action", action, self.current_step)
        self.current_step += 1
        return next_state, reward, done

    def episode(self):
        state = self.env.reset()
        score = 0
        done = False
        while not done:
            state, reward, done = self.timestep(state)
            score += reward
        self.writer.add_scalar("score", score, self.current_episode)
        self.current_episode += 1
        return score

    def main_loop(self):
        for episode in range(self.total_episode):
            self.episode()
            if episode % 100 == 0:
                self.main_net.save()
                self.write_net_hist()

if __name__ == '__main__':
    FQF(env=gym.make("CartPole-v1"), n_supports=8, hidden_size=128, learning_rate=1e-5, batch_size=8,
            total_episode=10000, epsilon_decay=0.9999, save_path="./save_model/model.pth").main_loop()