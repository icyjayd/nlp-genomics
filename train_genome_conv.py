from torch.utils.data import Dataset, DataLoader
from torch.nn.utils.rnn import pad_sequence
from torch import nn, optim
import torch
from tables import *
import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
import time
import math

class UHGGDatasetH5(Dataset):
    def __init__(self, df, path_to_db, pad_length=1069919, label_col = 'family', pad_token = 0):
        super().__init__()
        self.df = df
        self.idx_dict = dict(zip(np.arange(len(df)), list(df.index)))
        self.label_col = label_col
        self.class_dict = dict(zip(df[label_col].unique(), np.arange(len(df[label_col].unique()))))
        self.path = path_to_db
        self.file = open_file(path_to_db, 'r')
        self.data = self.file.root.data
        self.pad_length = pad_length
        self.pad_token = pad_token
    def __len__(self):
        return(len(self.df))
    def pad_to_length(self, tkns):
        if(len(tkns)<self.pad_length):
            tkns += [0] * (self.pad_length-len(tkns))
        else:
            tkns=tkns[:self.pad_length]
        return tkns
    def __getitem__(self, idx):
        index = self.idx_dict[idx]
        tokens = self.data['Tknz%d' % index].read()
        x = self.pad_to_length(tokens)
        x = torch.tensor(x)
        species_rep = self.df[self.label_col][index]
        y = self.class_dict[species_rep]
        y = torch.tensor(y).long()
        return (x.cuda(), y.cuda())

class GenomeConv(nn.Module):
    def __init__(self, embedding_length, embedding_size=40, out_size=10, dropout = 0.2, convs = None):
        super().__init__()
        self.emb = nn.Embedding(embedding_length, embedding_size)
        self.emb.weight.data.uniform_(-1, 1)
        dropout = nn.Dropout(dropout)
        if(convs == None):
            convs = [1, 2, 4, 6, 8, 10, 12, 14, 16]
        modules = []
        for i in range(1, len(convs)):
            modules.append(nn.Conv1d(convs[i-1] * embedding_size, 
                                     convs[i] *embedding_size, 
                                     kernel_size = 3, stride=2))
            modules.append(nn.ReLU())
            if(i%2 ==0):
                modules.append(dropout)
            modules.append(nn.MaxPool1d(kernel_size=3, stride=2))
        modules.append(nn.Flatten())
        modules.append(nn.Linear(15 * embedding_size * convs[-1], out_size))
        modules.append(nn.Sigmoid())
        self.net = nn.Sequential(*modules)

                
 
    def forward(self, x):
        x = self.emb(x)
        x = x.transpose(2, 1)
        x = self.net(x)
        return x


batch_size = 4
label_col = "family"
np.random.seed(42)
torch.manual_seed(42)
path = '/gpfs/data/johnsonslab/nlp-genomics/almeida-2020/'
path_to_db = os.path.join(path, 'tokenizations_8192k_poc.h5')
all_species = pd.read_csv(os.path.join(path, "all_species_clades.csv"))
family_counts = all_species['family'].value_counts()

samples = all_species[all_species['family'].isin(family_counts.index[:7])]
train_set, val_set = train_test_split(samples, test_size=0.2)
val_set, test_set = train_test_split(val_set, test_size=0.5)
vocab = 1069919

train_loader = DataLoader(UHGGDatasetH5(train_set, path_to_db, label_col=label_col,
                                        pad_token = 0, pad_length = vocab),
                        batch_size=batch_size, shuffle=True)#, collate_fn=Collater(vocab_size))#, num_workers=4)
val_loader = DataLoader(UHGGDatasetH5(val_set, path_to_db, label_col=label_col, 
                                      pad_token=0, pad_length = vocab),
                        batch_size=batch_size, shuffle=True)#, collate_fn=Collater(vocab_size))#, num_workers=4)
test_loader = DataLoader(UHGGDatasetH5(test_set, path_to_db, label_col = label_col, 
                                       pad_token=0, pad_length = vocab),
                        batch_size=batch_size, shuffle=True)#, collate_fn=Collater(vocab_size))#, num_workers=4)

CUDA_LAUNCH_BLOCKING=1
torch.cuda.empty_cache()
start_time = time.time()
num_epochs = 50

vocab_size = 8192000
embedding_length = 160
output_size = 8

acc_loss_path = '/gpfs/data/johnsonslab/nlp-genomics/almeida-2020/model_checkpoints/accuracy_loss_8192k_poc_10-27-23.csv'
acc_loss_df = pd.read_csv(acc_loss_path)
checkpoint_path = '/gpfs/data/johnsonslab/nlp-genomics/almeida-2020/model_checkpoints/model_parameters_8192k_10-27-23'

model = GenomeConv(vocab_size, embedding_size=embedding_length, out_size=8).cuda()
optimizer = optim.Adam(model.parameters(), lr=0.001)
loss_fn = nn.CrossEntropyLoss()

checkpoint = torch.load(checkpoint_path + "epoch_0")
model.load_state_dict(checkpoint['model_state_dict'])
optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
start_epoch = checkpoint['epoch'] + 1

for epoch in range(start_epoch, num_epochs):
    running_loss = 0.0
    epoch_time = time.time()
    model.train()
    for i, (x, y) in enumerate(train_loader):
        optimizer.zero_grad()
        out = model(x)
        loss = loss_fn(out, y)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
        if i % 4113 == 0:    # print every 10% of the dataset
            print(f'Train: [Epoch: {epoch + 1}, Minibatch: {i + 1:5d}] loss: {running_loss / (i+1):.3f}')#' epoch time: {time.time()-epoch_time}')
    print(f"Epoch time: {time.time()-epoch_time}")
    correct = 0
    total = 0

    predictions = []
    truths = []

    model.eval()
    for i,(x, y) in enumerate(val_loader):
        out = model(x)
        pred = torch.max(out, 1)[1]
        predictions += list(pred.cpu().numpy())
        truths += list(y.cpu().numpy())
        total += y.size(0)
        correct += (pred.cpu() == y.long().cpu()).sum()

        loss = loss_fn(out, y)
        running_loss += loss.item()
    acc = 1.0 * correct/total
    loss = running_loss/(i+1)
    torch.save({"epoch":epoch,
                "model_state_dict":model.state_dict(),
                "optimizer_state_dict":optimizer.state_dict(),
                "loss":loss
    }, checkpoint_path + "epoch_{}".format(epoch))
    
    
    acc_loss_slice = pd.DataFrame({"accuracy":[acc], "loss":[loss]})
    acc_loss_df = pd.concat([acc_loss_df, acc_loss_slice])
    acc_loss_df.to_csv(acc_loss_path)

    print(f'Val: [Epoch: {epoch + 1}] loss: {loss / 20:.3f} accuracy: {(acc * 100):.3f}')