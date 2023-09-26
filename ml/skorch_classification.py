import pandas as pd
import os
import numpy as np
from skorch import NeuralNetBinaryClassifier
from library import *

import torch
import torch.nn.functional as F
from torch import nn
from torch.utils.data import DataLoader
from torch.nn.utils.rnn import pad_sequence
from torch.utils.data import DataLoader, TensorDataset

from skorch.dataset import ValidSplit

import itertools


np.random.seed(RANDOM_STATE)

# Define the LSTM Network
class LSTMNetwork(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim=1, num_layers=2, dropout=0.2):
        super(LSTMNetwork, self).__init__()
        self.hidden_dim = hidden_dim

        # Define LSTM layer
        self.lstm1 = nn.LSTM(input_dim, hidden_dim, num_layers=num_layers)
        self.lstm2 = nn.LSTM(hidden_dim, hidden_dim//2, num_layers=num_layers)

        # Define dropout layer
        self.dropout = nn.Dropout(dropout)

        self.fc_input_size = hidden_dim//2 

        # Define output layer
        self.fc = nn.Linear(self.fc_input_size, output_dim)

    def forward(self, x):
        # LSTM layers
        lstm_out, _ = self.lstm1(x)
        lstm_out = F.relu(lstm_out)
        lstm_out, _ = self.lstm2(lstm_out)
        lstm_out = F.relu(lstm_out)

        # Take the last time step output from LSTM
        lstm_out = lstm_out[:, -1, :]

        # Dropout and fully connected layer
        out = self.dropout(lstm_out)
        out = self.fc(out)

        return out.squeeze(1)

# Use Skorch for training
input_dim = 4   # number of EEG channels
hidden_dim = 64  # number of neurons in the first hidden layer

Y_STYLE = 'elo'

LOWER_QUANTILE = 0.25
UPPER_QUANTILE = 0.75

print(f"loading file: {DBFNAME.split('.csv')[0]}_raw_{FILTNAME}")
raw_df = pd.read_csv(f"{DBFNAME.split('.csv')[0]}_raw_{FILTNAME}", dtype = {'pid': str})
raw_df = raw_df[raw_df['pid'].notna()] # drop all rows that have 'nan' in pid

PIDS = raw_df['pid'].unique()

def extract_features(df):
    p_dfs = {}
    global_id = 0
    for pid in df['pid'].unique():
        p_df = df[df['pid'] == pid].copy().reset_index(drop=True)
           
        lower = p_df['elo'].quantile(LOWER_QUANTILE)
        upper = p_df['elo'].quantile(UPPER_QUANTILE)

        if Y_STYLE == 'elo':            
            p_df = p_df[(p_df['elo'] <= lower) | (p_df['elo'] >= upper)].reset_index(drop=True)
            p_df['y'] = p_df['elo'] > lower
        else:            
            p_df['y'] = p_df['solved']

        p_df['block_id'] = p_df['block_id'].astype(int) + global_id
        global_id = p_df['block_id'].max() + 1

        p_dfs[pid] = p_df
    
    
    return p_dfs


def runKFold(X, y, pid, datatype):
 
    indices = list(range(len(X)))
    kf = KFold(n_splits=3, shuffle=True, random_state=RANDOM_STATE)

    reports = { model: [] for model in MODELS }
    for i, (train_indices, test_indices) in enumerate(kf.split(indices)):        
        train_indices = train_indices.tolist()
        test_indices = test_indices.tolist()        
        
        X_train, X_test = X[train_indices], X[test_indices]
        y_train, y_test = y[train_indices], y[test_indices]

        for model in MODELS:            
            model.fit(X_train, y_train)
            #print(classification_report(y_test, model.predict(X_test)))
            report = classification_report(y_test, model.predict(X_test), output_dict=True)
            reports[model].append(report['macro avg']['f1-score'])
    
    avgs = {model:np.mean(reports[model]) for model in reports}
    max_name_length = max(len(model.__class__.__name__) for model in avgs)

    # print best 3 models:
    avgs = {k: v for k, v in sorted(avgs.items(), key=lambda item: item[1], reverse=True)}
    for model, avg in avgs.items():
        print(f"{datatype} - pid - {pid} - {model.__class__.__name__:<{max_name_length}} - {avg:.3f}")
    
    print('---------------------------------')

def create_windows(data_dict, window_size, step_size):
    windowed_data = {}
    windowed_labels = {}

    for pnum, df in data_dict.items():
        # Drop the unnecessary columns
        df = df.drop(columns=['timestamp', 'pid', 'elo', 'solved'])

        # Create windows for each block
        block_windows = []
        block_labels = []
        for block_id in df['block_id'].unique():
            block_data = df[df['block_id'] == block_id]
            block_data = block_data.drop(columns=['block_id'])
            
            windows = []
            labels = []
            for i in range(0, len(block_data) - window_size + 1, step_size):
                window = block_data.iloc[i:i+window_size, :]
                windows.append(window.drop(columns=['y']).values)
                
                # Assign the label of the window to be the label of the last time point in the window
                labels.append(block_data['y'].iloc[i+window_size-1])

            block_windows.append(np.array(windows))
            block_labels.append(np.array(labels))

        windowed_data[pnum] = block_windows
        windowed_labels[pnum] = block_labels

    return windowed_data, windowed_labels

from sklearn.model_selection import train_test_split

def split_data(windowed_data, windowed_labels, test_size=0.25):
    train_data = {}
    test_data = {}
    train_labels = {}
    test_labels = {}

    for pnum in windowed_data.keys():
        participant_data = windowed_data[pnum]
        participant_labels = windowed_labels[pnum]

        # Create train and test split for each block
        train_block_data, test_block_data, train_block_labels, test_block_labels = [], [], [], []
        for block_data, block_labels in zip(participant_data, participant_labels):
            X_train, X_test, y_train, y_test = train_test_split(
                block_data, block_labels, test_size=test_size, shuffle=False
            )
            train_block_data.append(X_train)
            test_block_data.append(X_test)
            train_block_labels.append(y_train)
            test_block_labels.append(y_test)

        train_data[pnum] = train_block_data
        test_data[pnum] = test_block_data
        train_labels[pnum] = train_block_labels
        test_labels[pnum] = test_block_labels

    return train_data, test_data, train_labels, test_labels

window_size = 256  # 1 second of data at 256 Hz
step_size = window_size // 2  # 50% overlap

dfs = extract_features(raw_df)
data, labels = create_windows(dfs, window_size, step_size)
train_data, test_data, train_labels, test_labels = split_data(data, labels, test_size=0.2)


# Convert your data and labels to PyTorch tensors
train_data_tensors = [[torch.tensor(block.astype(float)) for block in pdata] for pdata in train_data.values()]
test_data_tensors = [[torch.tensor(block.astype(float)) for block in pdata] for pdata in test_data.values()]

train_label_tensors = [[torch.tensor(block.astype(float)) for block in pdata] for pdata in train_labels.values()]
test_label_tensors = [[torch.tensor(block.astype(float)) for block in pdata] for pdata in test_labels.values()]

train_data_tensors_filtered = []
train_labels_tensors_filtered = []
for pnum_data, pnum_labels in zip(train_data_tensors, train_label_tensors):
    for data_block, labels_block in zip(pnum_data, pnum_labels):
        if data_block.shape[0] < 10: continue 
        train_data_tensors_filtered.append(data_block[:10, :, :])
        train_labels_tensors_filtered.append(labels_block[:10])


train_data_tensors = torch.stack(train_data_tensors_filtered)
train_labels_tensors = torch.stack(train_labels_tensors_filtered)

train_unstacked = train_data_tensors.view(-1, 256, 4)
labels_unstacked = train_labels_tensors.view(-1)

train_data = torch.tensor(train_unstacked, dtype=torch.float32)
train_labels = torch.tensor(labels_unstacked, dtype=torch.float32)

net = NeuralNetBinaryClassifier(
    LSTMNetwork,
    module__input_dim=input_dim,
    module__hidden_dim=hidden_dim,
    criterion=torch.nn.BCEWithLogitsLoss,
    optimizer=torch.optim.Adam,
    max_epochs=10,
    train_split=ValidSplit(10),
    verbose=1
)

# X_train, X_val, y_train, y_val = train_test_split(train_data, train_labels, test_size=0.2, random_state=42)

# from skorch.dataset import Dataset
# valid_dataset = Dataset(X_val, y_val)

# Train the model
net.fit(train_data, train_labels)