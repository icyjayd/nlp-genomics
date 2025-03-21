import youtokentome as yttm
import os
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
from functools import partial
import itertools

directory ='/gpfs/data/johnsonslab/nlp-genomics/model_genomes/'
model_path = "/gpfs/data/johnsonslab/nlp-genomics/pasolli-2019/metagenomes_8192k.model"
bpe = yttm.BPE(model=model_path)


files = ['Bacteroides fragilis strain FDAARGOS_1225 chromosome, complete genome.fasta',
'Bifidobacterium adolescentis strain 1-11 chromosome, complete genome.fasta',
'Clostridioides difficile strain CD9501.fasta',
'Enterobacter cloacae strain GGT036 chromosome, complete genome.fasta',
'Escherichia coli str. K-12 substr. MG1655, complete genome.fasta',
'Fusobacterium nucleatum subsp. polymorphum strain NCTC10562 chromosome 1, complete sequence.fasta',
'Helicobacter pylori strain MT5135 chromosome, complete genome.fasta',
'Lactiplantibacillus plantarum strain SK151 chromosome, complete genome.fasta',
'Phocaeicola vulgatus ATCC 8482, complete sequence.fasta',
'Salmonella enterica subsp. enterica serovar Typhimurium str. LT2, complete genome.fasta']
names = ['B. fragilis', 'B. adolescentis','C. difficile', 'E. cloacae','E. coli', 'F. nucleatum',
        'H. pylori', 'L. plantarum', 'P. vulgatus', 'S. enterica']
families = ['Bacteroidaceae', 'Bifidobacteriaceae', 'Clostridiaceae', 'Enterobacteriaceae', 'Enterobacteriaceae','Fusobacteriaceae',
           'Helicobacteraceae', 'Lactobacillaceae','Bacteroidaceae', 'Enterobacteriaceae']

import pandas as pd
import numpy as np
from functools import partial
# with open('all_genomes_unlabeled_sample-A0.1-1.txt') as f:
#     length = sum(1 for line in f)
#     print('length:', length)
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
threshold = 0
tokenize = partial(tokenize_with_length_threshold, length_threshold = threshold)

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

def max_len(path):
    genomes = list(retrieve_genomes(path).values())
    maximum = -np.inf
    for genome in genomes:
        maximum = max(maximum, len(genome))
    return maximum
def min_len(path):
    genomes = list(retrieve_genomes(path).values())
    minimum = np.inf
    for genome in genomes:
        minimum = min(minimum, len(genome))
    return minimum
def mean_len(path):
    genomes = list(retrieve_genomes(path).values())
    total = 0
    for genome in genomes:
        total+= len(genome)
    if(len(genomes)>0):
        return total/len(genomes)
    else:
        return 0
def get_counts(path):
    genomes = list(retrieve_genomes(path).values())
    return len(genomes)
def get_ignore_dict(thresholds):
    ignore_dict = {}
    for threshold in thresholds:
        ignore_dict[threshold]=[]
        for vocab in bpe.vocab():
            if(len(vocab)<threshold):
                ignore_dict[threshold].append(vocab)
    return ignore_dict
def retrieve_tokenizations(files):
    tokenizations = []
    genome_lens = []
    for file in files:
        path = os.path.join(directory, file)
        genome = retrieve_genomes(path, gzipped=False)

        genome = genome[list(genome.keys())[0]]
        genome_lens.append(len(genome))
#         freqs = {}
        threshold = 0
        tokenizations.append(tokenize(genome, length_threshold=threshold))
    return tokenizations, genome_lens

tokenizations = []
genome_lens = []
for file in files:
    path = os.path.join(directory, file)
    genome = retrieve_genomes(path, gzipped=False)

    genome = genome[list(genome.keys())[0]]
    genome_lens.append(len(genome))
    freqs = {}
    threshold = 0
    tokenizations.append(tokenize(genome, length_threshold=threshold))
all_tokens = list(itertools.chain(*tokenizations))
all_tokens = set(all_tokens)

token_dict = {token: set() for token in all_tokens}
for i, tokenization in enumerate(tokenizations):
    #for each tokenization, assign a set of unique values
    token_set = (set(tokenization))
    for j, token in enumerate(all_tokens):
        #for each token, check if the unique value exists in the tokenization

        if token in token_set:
            token_dict[token].add(i)

        if(token=='GTGCGGATAGTTTTCTGCGTAAT'):
            print(token_dict['GTGCGGATAGTTTTCTGCGTAAT'])

universal_token_list = []
isolated_token_list = []
shared_token_list = []

for token_family in token_dict.items():
    if(len(token_family[1])==len(names)):
        universal_token_list.append(token_family[0])
    elif(len(token_family[1])==1):
        isolated_token_list.append(token_family[0])
    else:
        shared_token_list.append(token_family[0])

universal_token_list = sorted(universal_token_list, key=len, reverse=True)
isolated_token_list = sorted(isolated_token_list, key=len, reverse=True)
shared_token_list = sorted(shared_token_list, key=len, reverse=True)
univ_count = 0
iso_count = 0
share_count = 0
for tokenization in tokenizations:
    for token in tokenization:
        if(token in universal_token_list):
            univ_count += 1
        elif(token in isolated_token_list):
            iso_count += 1
        else:
            share_count +=1
print(univ_count)
print(iso_count)
print(share_count)
