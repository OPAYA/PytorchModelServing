'''
    code by Juntae Kim
'''

from torch.utils.data import DataLoader, Dataset
import numpy as np
import torch
class dataset(Dataset):
    def __init__(self, data):
        self.x, self.y = data
    
    def __getitem__(self, index):
        return self.x[index], self.y[index]

    def __len__(self):
        return len(self.x)

def dataloader():
    x_train = np.load('data/x_train.npy')
    x_train = torch.tensor(x_train).squeeze(1).reshape(-1, 1, 28, 28).float()
    y_train = np.load('data/y_train.npy')
    y_train = torch.tensor(y_train).long()

    x_test = np.load('data/x_test.npy')
    x_test = torch.tensor(x_test).squeeze(1).reshape(-1, 1, 28,28).float()
    y_test = np.load('data/y_test.npy')
    y_test = torch.tensor(y_test).long()

    train_data = x_train, y_train
    val_data = x_test, y_test
    
    train_dataset = dataset(train_data)
    val_dataset = dataset(val_data)
    
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)
    return train_loader, val_loader
