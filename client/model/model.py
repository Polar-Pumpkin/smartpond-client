import numpy as np
import torch
import torch.nn.functional as F
from torch import nn


# 这是一个用于生成批次数据的函数，主要用于时间序列预测任务。函数的输入参数包括：
# - X:一个形状为(num_samples, train_periods, num_features)的数组，表示样本的特征数据。
# - y:一个形状为(num_samples, train_periods)的数组，表示样本的目标值。
# - num_obs_to_train:一个整数，表示训练的历史窗口长度。
# - seq_len:一个整数，表示序列/编码器/解码器的长度。
# - batch_size:一个整数，表示每个批次的大小。
# 函数的主要步骤如下：
# 1. 首先，获取X的形状，然后检查batch_size是否大于X的样本数量，如果是，则将batch_size设置为X的样本数量。
# 2. 然后，从num_obs_to_train和num_periods - seq_len - 1之间随机选择一个整数作为预测点t。
# 3. 接着，从X的所有样本中随机选择batch_size个样本作为当前批次的数据。
# 4. 根据选定的批次和预测点t,从X中提取出训练批次的特征数据X_train_batch和目标值y_train_batch。
# 5. 从X中提取出预测点的前seq_len个时间步的特征数据Xf和目标值yf。
# 6. 最后，返回训练批次的特征数据X_train_batch、目标值y_train_batch、预测点的前seq_len个时间步的特征数据Xf和目标值yf。

# model
class Gaussian(nn.Module):

    def __init__(self, hidden_size, output_size):
        '''
        Gaussian Likelihood Supports Continuous Data
        Args:
        input_size (int): hidden h_{i,t} column size
        output_size (int): embedding size
        '''
        super(Gaussian, self).__init__()
        self.mu_layer = nn.Linear(hidden_size, output_size)
        self.sigma_layer = nn.Linear(hidden_size, output_size)

    # 这是一个定义高斯似然模型的PyTorch类。这个类继承了nn.Module, 用于处理连续数据。
    # 在这个类中，有两个线性层：mu_layer和sigma_layer。mu_layer的输入大小是hidden_size, 输出大小是output_size;
    # sigma_layer的输入大小也是hidden_size, 输出大小同样是output_size。这两个线性层的权重和偏置都是在初始化时设定的。
    # initialize weights
    # nn.init.xavier_uniform_(self.mu_layer.weight)
    # nn.init.xavier_uniform_(self.sigma_layer.weight)

    def forward(self, h):  # h为神经网络隐藏层输出 (batch, hidden_size)
        _, hidden_size = h.size()
        sigma_t = torch.log(1 + torch.exp(self.sigma_layer(h))) + 1e-6
        mu_t = self.mu_layer(h)
        return mu_t, sigma_t  # (batch, output_size)


# 一个前向传播函数，用于计算高斯分布的均值(mu_t)和标准差(sigma_t)。
# 输入参数h是神经网络隐藏层的输出，形状为(batch, hidden_size)。
# 获取h的形状，然后通过sigma_layer和mu_layer分别计算sigma_t和mu_t。sigma_t是通过将h传入sigma_layer得到的，
# 然后取指数并加1,再取对数并加上一个很小的数(1e-6)来防止log(0)的情况。mu_t是通过将h传入mu_layer得到的。
# 最后，返回mu_t和sigma_t,它们的形状都是(batch, output_size)。

class NegativeBinomial(nn.Module):

    def __init__(self, input_size, output_size):
        '''
        Negative Binomial Supports Positive Count Data
        Args:
        input_size (int): hidden h_{i,t} column size
        output_size (int): embedding size
        '''
        super(NegativeBinomial, self).__init__()
        self.mu_layer = nn.Linear(input_size, output_size)
        self.sigma_layer = nn.Linear(input_size, output_size)

    # 这是一个定义负二项分布模型的PyTorch类。这个类继承了nn.Module,用于处理正计数数据。

    # 在这个类中，有两个线性层：mu_layer和sigma_layer。mu_layer的输入大小是input_size,\
    # 输出大小是output_size;sigma_layer的输入大小也是input_size,输出大小同样是output_size。
    # 这两个线性层的权重和偏置都是在初始化时设定的。
    def forward(self, h):  # h为神经网络隐藏层输出 (batch, hidden_size)
        _, hidden_size = h.size()
        alpha_t = torch.log(1 + torch.exp(self.sigma_layer(h))) + 1e-6
        mu_t = torch.log(1 + torch.exp(self.mu_layer(h)))
        return mu_t, alpha_t  # (batch, output_size)


def gaussian_sample(mu, sigma):
    gaussian = torch.distributions.normal.Normal(mu, sigma)
    ypred = gaussian.sample()
    return ypred  # (num_ts, 1)


# 这是一个用于生成高斯分布样本的函数。
# 输入参数mu和sigma分别是高斯分布的均值和标准差。
# 在函数中，首先使用torch.distributions.normal.Normal创建一个正态分布对象gaussian,然后调用其sample方法生成一个样本ypred。
# 最后，返回ypred,它的形状是(num_ts, 1),其中num_ts是时间序列的长度。

def negative_binomial_sample(mu, alpha):
    var = mu + mu * mu * alpha
    ypred = mu + torch.randn() * torch.sqrt(var)
    return ypred


# deepar
class DeepAR(nn.Module):

    def __init__(self, input_size, embedding_size, hidden_size, num_layers, lr=1e-3, likelihood="g", device=None):
        super(DeepAR, self).__init__()
        self.device = device

        # network
        self.input_embed = nn.Linear(1, embedding_size)
        self.encoder = nn.LSTM(embedding_size + input_size, hidden_size,
                               num_layers, bias=True, batch_first=True)
        if likelihood == "g":
            self.likelihood_layer = Gaussian(hidden_size, 1)
        elif likelihood == "nb":
            self.likelihood_layer = NegativeBinomial(hidden_size, 1)
        self.likelihood = likelihood

    # 这是一个定义深度自回归模型(DeepAR)的PyTorch类。这个类继承了nn.Module,用于处理时间序列数据。
    # input_embed:一个线性层，将输入的时间序列数据转换为嵌入向量。输入的大小是1,输出的大小是embedding_size。
    # encoder:一个LSTM层，用于对嵌入向量进行编码。输入的大小是(embedding_size + input_size),输出的大小是hidden_size,隐藏状态的大小也是hidden_size。num_layers表示LSTM的层数。bias=True表示使用偏置项，batch_first=True表示输入和输出的第一个维度都是批次大小。
    # likelihood_layer:根据参数likelihood的值选择不同的似然函数层。如果likelihood等于"g",则使用高斯分布；如果likelihood等于"nb",则使用负二项分布。这两个层的输入大小都是hidden_size,输出的大小都是1。
    def forward(self, X, y, Xf):
        if isinstance(X, type(np.empty(2))):  # 转换为tensor
            X = torch.from_numpy(X).float()
            y = torch.from_numpy(y).float()
            Xf = torch.from_numpy(Xf).float()
        num_ts, num_obs_to_train, _ = X.size()
        _, seq_len, num_features = Xf.size()
        ynext = None
        ypred = []
        mus = []
        sigmas = []
        h, c = None, None
        # 遍历所有时间点
        for s in range(num_obs_to_train + seq_len):  # num_obs_to_train为历史序列长度，seq_len为预测长度
            if s < num_obs_to_train:  # Encoder，ynext为真实值
                if s == 0:
                    ynext = torch.zeros((num_ts, 1))
                    if self.device:
                        ynext = ynext.to(self.device)
                else:
                    ynext = y[:, s - 1].view(-1, 1)  # (num_ts,1) # 取上一时刻的真实值
                yembed = self.input_embed(ynext).view(num_ts, -1)  # (num_ts,embedding_size)
                x = X[:, s, :].view(num_ts, -1)  # (num_ts,num_features)
            else:  # Decoder，ynext为预测值
                if s == num_obs_to_train: ynext = y[:, s - 1].view(-1, 1)  # (num_ts,1) # 预测的第一个时间点取上一时刻的真实值
                yembed = self.input_embed(ynext).view(num_ts, -1)  # (num_ts,embedding_size)
                x = Xf[:, s - num_obs_to_train, :].view(num_ts, -1)  # (num_ts,num_features)
            x = torch.cat([x, yembed], dim=1)  # (num_ts, num_features + embedding)
            inp = x.unsqueeze(1)  # (num_ts,1, num_features + embedding)

            if h is None and c is None:
                out, (h, c) = self.encoder(inp)  # h size (num_layers, num_ts, hidden_size)
            else:
                out, (h, c) = self.encoder(inp, (h, c))
            hs = h[-1, :, :]  # (num_ts, hidden_size)
            hs = F.relu(hs)  # (num_ts, hidden_size)
            mu, sigma = self.likelihood_layer(hs)  # (num_ts, 1)
            mus.append(mu.view(-1, 1))
            sigmas.append(sigma.view(-1, 1))
            if self.likelihood == "g":
                ynext = gaussian_sample(mu, sigma)
                # (num_ts, 1)
            elif self.likelihood == "nb":
                alpha_t = sigma
                mu_t = mu
                ynext = negative_binomial_sample(mu_t, alpha_t)  # (num_ts, 1)
            # if without true value, use prediction
            if num_obs_to_train <= s < num_obs_to_train + seq_len:  # 在预测区间内
                ypred.append(ynext)
        ypred = torch.cat(ypred, dim=1).view(num_ts, -1)  # (num_ts, seq_len)
        mu = torch.cat(mus, dim=1).view(num_ts, -1)  # (num_ts, num_obs_to_train + seq_len)
        sigma = torch.cat(sigmas, dim=1).view(num_ts, -1)  # (num_ts, num_obs_to_train + seq_len)
        return ypred, mu, sigma
