import os
from enum import Enum
from typing import List, Optional

import numpy as np
import pandas as pd
import torch
from tqdm import tqdm

from model import DeepAR
from scaler import Scaler, MeanScaler

num_obs_to_train = 168  # 训练的历史窗口长度
seq_len = 30  # 预测的未来窗口长度
sample_size = 100
embedding_size = 10  # 将上一时刻的真实值编码为embedding_size长度
hidden_size = 100
n_layers = 1
lr = 1e-3
likelihood = 'g'


class Field(Enum):
    TIMESTAMP = '时间'
    WATERTEMP = '温度'
    DO = '溶解氧'
    PH = 'pH'
    NH3N = '氨氮'
    NO3N = '硝氮'
    SKYCON = '天气状况'
    WINDSPEED = '风速'
    AIRTEMP = '气温'

    YEAR = '年'
    MONTH = '月'
    DAY = '日'
    HOUR = '时'


device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
columns = list(map(lambda x: x.value, [
    Field.TIMESTAMP,
    Field.WATERTEMP,
    Field.DO,
    Field.PH,
    Field.NH3N,
    Field.NO3N,
    Field.SKYCON,
    Field.WINDSPEED,
    Field.AIRTEMP
]))


# noinspection PyPep8Naming
def RSE(ypred, ytrue):
    rse = np.sqrt(np.square(ypred - ytrue).sum()) / np.sqrt(np.square(ytrue - ytrue.mean()).sum())
    return rse


# noinspection PyPep8Naming
def MAPE(ytrue, ypred):
    ytrue = np.array(ytrue).ravel() + 1e-4
    ypred = np.array(ypred).ravel()
    return np.mean(np.abs((ytrue - ypred) / ytrue))


def sliding_window(data_set, width, multi_vector=True):  # DataSet has to be as an Array
    if multi_vector:  # 三维 (num_samples,length,features)
        num_samples, length, featuress = data_set.shape
        x = data_set[:, 0:width, :]  # (num_samples,width,features)
        x = x[np.newaxis, :, :, :]  # (1,num_samples,width,features)
        for i in range(length - width):
            i += 1
            tmp = data_set[:, i:i + width, :]  # (num_samples,width,features)
            tmp = tmp[np.newaxis, :, :, :]  # (1,num_samples,width,features)
            x = np.concatenate([x, tmp], 0)  # (i+1,num_samples,width,features)
            return x
    else:
        # 二维 (num_samples,length)
        data_set = data_set[:, :, np.newaxis]  # (num_samples,length,1)
        num_samples, length, featuress = data_set.shape
        x = data_set[:, 0:width, :]  # (num_samples,width,features)
        x = x[np.newaxis, :, :, :]  # (1,num_samples,width,features)
        for i in range(length - width):
            i += 1
            tmp = data_set[:, i:i + width, :]  # (num_samples,width,features)
            tmp = tmp[np.newaxis, :, :, :]  # (1,num_samples,width,features)
            x = np.concatenate([x, tmp], 0)  # (i+1,num_samples,width,features)
            return x


'''def update(X):
    num_ts, num_periods, num_features = X.shape
    model = DeepAR(num_features, embedding_size, hidden_size, n_layers, lr, likelihood, device=device)
    orginal_weight = model.state_dict()
 '''

width = num_obs_to_train + seq_len


def run(field: str, values: pd.DataFrame, scaler: Optional[Scaler] = None):  # -> Tuple[float,float,float]:
    frame = pd.DataFrame(np.array(values), columns=columns)
    frame[Field.TIMESTAMP.value] = pd.to_datetime(frame[Field.TIMESTAMP.value], format='%Y/%m/%d %H:%M')
    frame[Field.YEAR.value] = frame[Field.TIMESTAMP.value].apply(lambda x: x.year)
    frame[Field.MONTH.value] = frame[Field.TIMESTAMP.value].apply(lambda x: x.month)
    frame[Field.DAY.value] = frame[Field.TIMESTAMP.value].apply(lambda x: x.day)
    frame[Field.HOUR.value] = frame[Field.TIMESTAMP.value].apply(lambda x: x.hour)
    frame = frame.groupby(Field.TIMESTAMP.value).mean()
    # frame = frame.drop('timestamp', axis=1)
    for col in columns:
        if col != Field.TIMESTAMP.value:
            frame[col] = pd.to_numeric(frame[col])
            frame[col] = round(frame[col], 2)
    # for i in range(len(frame.columns)):
    #     frame[frame.columns[i]] = round(frame[frame.columns[i]], 2)
    cols = [col for col in frame.columns if col not in [field, Field.YEAR.value, Field.DAY.value] if
            frame[col].dtype != 'object']  # 处理目标的其他所有特征
    labels = []
    values = []
    for col in cols:
        labels.append(col)
        values.append(np.corrcoef(frame[col].values, frame[field].values)[0, 1])

    corr_frame = pd.DataFrame({'col_labels': labels, 'corr_values': values})
    sorted_indices = np.argsort(np.abs(values))[::-1]
    top_labels = [corr_frame.iloc[index]['col_labels'] for index in sorted_indices[:5]]
    selected_labels = list(map(str, top_labels))
    print(selected_labels)
    # X = np.asarray(list(map(lambda x: frame[x], selected_labels)))
    X = np.c_[np.asarray(frame[selected_labels[0]]), np.asarray(frame[selected_labels[1]]), np.asarray(
        frame[selected_labels[2]]), np.asarray(frame[selected_labels[3]]), np.asarray(frame[selected_labels[4]])]
    num_periods, num_features = len(frame), X.shape[1]
    X = X.reshape((-1, num_periods, num_features))
    Y = np.asarray(frame[field]).reshape((-1, num_periods))
    width = num_obs_to_train + seq_len
    Y = sliding_window(Y, width, multi_vector=False)  # (len-width+1,num_samples,width,1)
    X = sliding_window(X, width, multi_vector=True)
    if scaler:
        Y = scaler.fit_transform(Y)
    X = torch.from_numpy(X).to(dtype=torch.float32)
    Y = torch.from_numpy(Y).to(dtype=torch.float32)
    X = X[:, 0, :, :]
    Y = Y[:, 0, :, 0]
    num_ts, num_periods, num_features = X.shape
    model = DeepAR(num_features, embedding_size, hidden_size, n_layers, lr, likelihood, device=device)
    model.load_state_dict(torch.load(os.path.join('weight', f'{field}[best].pth')))
    # orginal_weight = model.state_dict()
    # model= torch.load(f'{name}_best.pth')
    model.eval()
    # X = X[:, :, :].reshape(-1, num_obs_to_train + seq_len, num_features).to(device)
    # Y = Y[:, :].reshape(-1, num_obs_to_train, seq_len).to(device)
    X_test = X[:, :num_obs_to_train, :]
    Xf_test = X[:, -seq_len:, :]
    Y_test = Y[:, :num_obs_to_train]
    Yf_test = Y[:, -seq_len:]
    X_test[torch.isnan(X_test)] = 1
    Xf_test[torch.isnan(Xf_test)] = 1
    Y_test[torch.isnan(Y_test)] = 1
    Yf_test[torch.isnan(Yf_test)] = 1
    Y_test = scaler.transform(Y_test)
    result = []
    n_samples = sample_size  # 采样个数

    for _ in tqdm(range(n_samples)):
        y_pred, _, _ = model(X_test, Y_test, Xf_test)  # ypred:(num_samples, seq_len)4
        y_pred = y_pred.cpu().numpy()
        y_pred = scaler.inverse_transform(y_pred)
        result.append(y_pred[:, :, np.newaxis])
    result = np.concatenate(result, axis=2)  # (num_samples, seq_len, n_samples)
    p50 = np.quantile(result, 0.5, axis=2)  # (num_samples, seq_len)
    # p90 = np.quantile(result, 0.9, axis=2) # (num_samples, seq_len)
    # p10 = np.quantile(result, 0.1, axis=2)
    pred_mid = p50[:, :].reshape(-1, seq_len)  # (num_samples,seq_len)
    true = Yf_test.cpu().detach().numpy()[:, :].reshape(-1, seq_len)  # (num_samples,seq_len)
    test_samples, seq_lenn = true.shape
    # 5. P50 quantile MAE
    MAE = 0
    for i in range(test_samples):
        error = 0
        for j in range(seq_len):
            error += np.abs(true[i, j] - pred_mid[i, j])
        mae = error / seq_len
        MAE += mae
    MAE = MAE / test_samples
    print("P50 quantile MAE:", MAE)

    # 6. # P50 quantile MAPE
    MAPe = 0
    for i in range(test_samples):
        mape = MAPE(true[i, :], pred_mid[i, :])
        MAPe += mape
    MAPe = MAPe / test_samples
    print("P50 quantile MAPE: {}".format(MAPe))
    return pred_mid


if __name__ == '__main__':
    data = pd.read_csv(os.path.join('..', '..', 'weight', 'test_data.csv'))
    fields = [Field.DO, Field.WATERTEMP, Field.PH, Field.NH3N, Field.NO3N]
    values = []
    for field in fields:
        value = run(field.value, data, MeanScaler())
        print(value)
