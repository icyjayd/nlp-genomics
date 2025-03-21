import youtokentome as yttm
from tables import *
import argparse
import pandas as pd
import os

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

if __name__ == "__main__":
    parser =argparse.ArgumentParser(description="Perform SVD random forest on TF-IDF metagenomes")
    parser.add_argument("model", type=str)
    args = parser.parse_args()
    model = args.model
    model_path = f'/gpfs/data/johnsonslab/nlp-genomics/pasolli-2019/metagenomes_{model}.model'
    bpe = yttm.BPE(model=model_path)
    path = '/gpfs/data/johnsonslab/nlp-genomics/alzheimers/ferreiro-2023'
    df = pd.read_csv(os.path.join(path, 'key_df.csv'))
    raw_file = open_file(os.path.join(path, f'raw_tokenizations_{model}.h5'), 'w')
    raw_group = raw_file.create_group('/', "data", "Tokenization Data")
    kneaded_file = open_file(os.path.join(path, f'kneaded_tokenizations_{model}.h5'), 'w')
    kneaded_group = kneaded_file.create_group('/', "data", "Tokenization Data")
    for sample_title in df['sample_title']:
        kneaded_tokens = tokenize(sample_title, 'megahit_kneaded_out', out='id')
        kneaded_file.create_array("/data", 'Tknz%d'% sample_title, kneaded_tokens)
        raw_tokens = tokenize(sample_title, 'megahit_raw_out', out='id')
        raw_file.create_array("/data", 'Tknz%d'% sample_title, raw_tokens)
    raw_file.close()
    kneaded_file.close()
    print(f'finished run with {model} model')
