import pandas as pd
import numpy as np
import os
os.chdir('/gpfs/data/johnsonslab/nlp-genomics/pasolli-2019')
def retrieve_genomes(path):
    with open(path, 'r') as f:
        file_content = f.readlines()
        file_content = [content.strip() for content in file_content]
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
    

folders = []
for file in os.listdir():
    if("tar" not in file and "txt" not in file and "model" not in file and "." not in file):
        folders.append(file)
files =[]
for folder in folders:
    for file in os.listdir(folder):
        #extract genomes from each file
        files.append(os.path.join(folder, file))
df = pd.DataFrame(index=np.arange(len(files)))
df['path'] = files
df['max_length'] = df['path'].apply(lambda x: max_len(x))
df['min_length'] = df['path'].apply(lambda x: min_len(x))
df['mean_length'] = df['path'].apply(lambda x: mean_len(x))
df['count'] = df['path'].apply(lambda x: get_counts(x))
df.to_csv('/gpfs/data/johnsonslab/nlp-genomics/pasolli-2019/sample_details.csv', index=None)