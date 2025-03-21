import os
import pandas as pd
import youtokentome as yttm
from functools import partial
import gzip
from BCBio import GFF
from functools import partial
model_path = "/gpfs/data/johnsonslab/nlp-genomics/pasolli-2019/metagenomes_8192k.model"
import torch
from torch import nn, optim
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
import numpy as np
import time
bpe = yttm.BPE(model=model_path)

def retrieve_genomes(path, gzipped=False):
    if(gzipped):
        with gzip.open(path, 'r') as f:
            file_content = f.readlines()
            file_content = [content.strip() for content in file_content]

    else:
        with open(path, 'r') as f:
            file_content = f.readlines()
            file_content = [content.strip() for content in file_content]
    if isinstance(file_content[0], bytes):
        file_content = [line.decode('utf') for line in file_content]
    genomes = {}
    bases = ""
    header = file_content[0]

    for i in range(1, len(file_content)):
        if(">") in file_content[i]:
            genomes[header] = bases
            header = file_content[i]
            bases=""
        else:
            bases+= file_content[i]
            if(i==len(file_content)-1):
                genomes[header] = bases
                header = file_content[i]
                bases=""
    return genomes

def retrieve_genome_from_gff(in_file):
    with(open(in_file)) as in_handle:
        return "".join([str(rec.seq) for rec in GFF.parse(in_handle)])

def tokenize_with_length_threshold(string, length_threshold=100):
    tokens= bpe.encode(string, output_type =yttm.OutputType.SUBWORD )
    out = []
    for token in tokens:
        if(len(token)>=length_threshold):
            out.append(token)
    if(len(out)==0):
        out.append("none")
#     print(len(tokens), len(out))
    return out

def get_clades(filename, df):
    idx = filename[:-4]
    lineage = df.loc[idx].Lineage
    domain = lineage[lineage.find('d__')+3:lineage.find(';')]
    phylum_start_idx = lineage.find('p__')+3
    phylum_end_idx = lineage[phylum_start_idx:].find(';')+phylum_start_idx
    phylum = lineage[phylum_start_idx:phylum_end_idx]
    class_start_idx = lineage.find('c__')+3
    class_end_idx = lineage[class_start_idx:].find(';')+class_start_idx
    class_ = lineage[class_start_idx:class_end_idx] #named so as not to break python
    order_start_idx = lineage.find('o__')+3
    order_end_idx = lineage[order_start_idx:].find(';')+order_start_idx
    order = lineage[order_start_idx:order_end_idx]
    family_start_idx = lineage.find('f__')+3
    family_end_idx = lineage[family_start_idx:].find(';')+family_start_idx
    family = lineage[family_start_idx:family_end_idx]
    genus_start_idx = lineage.find('g__')+3
    genus_end_idx = lineage[genus_start_idx:].find(';')+genus_start_idx
    genus = lineage[genus_start_idx:genus_end_idx]
    species = get_name_from_file(filename, df)
    return domain, phylum, class_, order, family, genus, species


    return domain, phylum
def get_name_from_file(filename, df):
    idx = filename[:-4]
    lineage = df.loc[idx].Lineage
    name = lineage[lineage.find('s__')+3:lineage.find('s__')+4] + "." + lineage[lineage.rfind(" "):]
    return name
def get_species_status(filename, df):
    if(filename[:-4] not in df.index):
        return False
    name = get_name_from_file(filename, df)
    if(name=="._"):
        return False
    else:
        return True



threshold = 0
tokenize = partial(tokenize_with_length_threshold, length_threshold = threshold)

class UHGGDataset(Dataset):
    def __init__(self, df, bpe, path_to_files, pad_length=500000, label_col = 'Species_rep'):
        self.df = df
        self.bpe = bpe
        self.idx_dict = dict(zip(np.arange(len(df)), list(df.index)))
        self.label_col = label_col
        self.class_dict = dict(zip(df[label_col].unique(), np.arange(len(df[label_col].unique()))))
#         print(len(df), len(self.class_dict.keys()))
        self.path = path_to_files
        self.pad_length = pad_length
    def __len__(self):
        return(len(self.df))
    def pad_to_length(self, tkns):
        if(len(tkns)<self.pad_length):
            tkns += [0] * (self.pad_length-len(tkns))
        else:
            tkns=tkns[:self.pad_length]
        return tkns
    def __getitem__(self, idx):
        name = self.idx_dict[idx]
        seq = retrieve_genome_from_gff(os.path.join(self.path, name + ".gff"))
        tokens = self.bpe.encode(seq)
        x = self.pad_to_length(tokens)
        x = torch.tensor(x)
        species_rep = self.df.loc[name][self.label_col]
        y = self.class_dict[species_rep]
        y = torch.tensor(y).long()
        return x.cuda(), y.cuda()

class GenomeNet(nn.Module):
    def __init__(self, embedding_length, embedding_size=40, out_size=10):
        super().__init__()
        self.emb = nn.Embedding(embedding_length, embedding_size)
#         self.convs = nn.Sequential(self.ConvBlock(1, 4, 3), self.ConvBlock(4, 8, 3),
#                                   self.ConvBlock(8,16,3), self.ConvBlock(8, 32, 3))
        self.convs = nn.Sequential(nn.Conv1d(40, 80, 7, stride=2),nn.ReLU(),
                                   nn.Conv1d(80, 160, 5, stride=2),nn.ReLU(),
                                  nn.Conv1d(160, 320, 3, stride=2),nn.ReLU(),
                                   nn.Conv1d(320, 512, 3, stride=2),nn.ReLU(),
                                  nn.Conv1d(512, 128, 3, stride=2),
                                  nn.Conv1d(128, 32, 3, stride=2),
                                  nn.Conv1d(32, 4, 3, stride=2))
        self.linear = nn.Sequential(nn.Linear(15620, out_size), nn.ReLU())
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.emb(x)
        x = x.reshape(x.shape[0], x.shape[2], x.shape[1])
        x = self.convs(x)
        x = x.reshape(x.shape[0], x.shape[1]*x.shape[2])
        x = self.linear(x)
        return x
#         return self.transformer(x)


model = GenomeNet(8192000).cuda()

path = '/gpfs/data/johnsonslab/nlp-genomics/almeida-2020/'
df = pd.read_csv(os.path.join(path, 'genomes-all_metadata.tsv'), sep='\t', index_col=0)
## Temporary code for not fully downloaded dataset
files = os.listdir(os.path.join(path, 'gffs'))
files = [file[:-4] for file in files]
df = df.loc[files]
idx = df['Country'].value_counts().index
print((df['Country'].value_counts()))
df = df[df['Country'].isin(idx[:10])]

batch_size = 8
label_col = "Country"
np.random.seed(42)
train_set, val_set = train_test_split(df, test_size=0.3)
val_set, test_set = train_test_split(val_set, test_size=0.5)

train_loader = DataLoader(UHGGDataset(train_set, bpe, os.path.join(path + "gffs"), label_col=label_col),batch_size=batch_size, shuffle=True)
val_loader = DataLoader(UHGGDataset(val_set, bpe, os.path.join(path + "gffs"), label_col=label_col),batch_size=batch_size, shuffle=True)
test_loader = DataLoader(UHGGDataset(test_set, bpe, os.path.join(path + "gffs"), label_col = label_col),batch_size=batch_size, shuffle=True)

start_time = time.time()
num_epochs = 50
model = GenomeNet(8192000).cuda()
optimizer = optim.Adam(model.parameters(), lr=0.001)
loss_fn = nn.CrossEntropyLoss()
for epoch in range(num_epochs):
    print("Starting epoch {}".format(epoch + 1))
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
#         loss = 0
        if i % 20== 19:    # print every 20 mini-batches
            print(f'Train: [{epoch + 1}, {i + 1:5d}] loss: {running_loss / 20:.3f} epoch time: {time.time()-epoch_time}')
            running_loss = 0.0
    running_loss = 0
    torch.save({
            'epoch': epoch,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
    }, '/gpfs/data/johnsonslab/nlp-genomics/model_weights/geneomenet_conv_weights/genomenet_conv_epoch_{}'.format(epoch))
    running_loss = 0

    print(f"Epoch time: {time.time()-start_time}")
    model.eval()
    for i,(x, y) in enumerate(val_loader):
        out = model(x)
        loss = loss_fn(out, y)
        running_loss += loss.item()
    print(f'Val: [{epoch + 1}, {i + 1:5d}] loss: {running_loss / 20:.3f}')
