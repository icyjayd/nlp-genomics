import os
import numpy as np
import pandas as pd
import tables
from tables import *
import pandas as pd
import os
import youtokentome as yttm
model_path = "/gpfs/data/johnsonslab/nlp-genomics/pasolli-2019/metagenomes_8192k.model"
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

def tokenize(sample_title, folder, out='subword',path='/gpfs/data/johnsonslab/nlp-genomics/alzheimers/ferreiro-2023'):
#     print("tokenizing", sample_title)
    file = os.path.join(path, str(sample_title), folder, 'final.contigs.fa')
    genomes = retrieve_genomes(file).values()
    tokens = []
    if out == 'subword':
        output_type = yttm.OutputType.SUBWORD
    elif out=='id':
        output_type = yttm.OutputType.ID
    for genome in genomes:
        tokens += bpe.encode(genome, output_type =output_type)
    return tokens
path = '/gpfs/data/johnsonslab/nlp-genomics/alzheimers/ferreiro-2023/'
df = pd.read_csv(os.path.join(path, 'key_df.csv'))

##raw
#need to remove missing index too
#idx = df[df['sample_title']==61707].index[0]

##kneaded
#idx = df[df['sample_title']==25632].index[0]
#df = pd.concat([df.iloc[:idx], df.iloc[idx + 1:]])

with open_file(os.path.join(path, "raw_tokenizations_8192k.h5"), 'w') as h5file:
    group = h5file.create_group('/', "data", "Tokenization Data")
    for sample_title in (df['sample_title']):
        tokens = tokenize(sample_title, 'megahit_raw_out', out='id')
        h5file.create_array("/data", 'Tknz%d'% sample_title, tokens)

