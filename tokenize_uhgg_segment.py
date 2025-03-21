import pandas as pd
import argparse
import os
import youtokentome as yttm
from functools import partial
from BCBio import GFF
import time
import numpy as np
def select_df(df, idx, length = 5000):
    idx = idx * length
    if(idx + length>len(df[idx:])):
        return df[idx:]
    else:
        return df[idx:idx + length]
def tokenize_df(df, idx, bpe, path):
    pool_handler(df)
#    for name in df.index:
#        seq = retrieve_genome_from_genome_name(name)
#        np.save(os.path.join(path, 'tokenizations', name+'.np'),np.array(bpe.encode(seq)))

def tokenize_from_name(name):
    seq = retrieve_genome_from_genome_name(name)
    tokens = np.array(bpe.encode(seq))
    np.save(os.path.join('/gpfs/data/johnsonslab/nlp-genomics/almeida-2020/tokenizations', name), tokens)
def pool_handler(df):
    p = Pool(40)
    p.map(tokenize_from_name, df.index)

def retrieve_genome_from_gff(in_file):
    with(open(os.path.join('/gpfs/data/johnsonslab/nlp-genomics/almeida-2020/gffs/',in_file + '.gff'))) as in_handle:
        return "".join([str(rec.seq) for rec in GFF.parse(in_handle)])
def retrieve_genome_from_genome_name(name):
    with(open(os.path.join('/gpfs/data/johnsonslab/nlp-genomics/almeida-2020/gffs/',name + '.gff'))) as in_handle:
        return "".join([str(rec.seq) for rec in GFF.parse(in_handle)])

def parse_args():
    parser=argparse.ArgumentParser(description="A script to pretokenize a section of the UHGG genomes")
    parser.add_argument("idx", type=int)
    parser.add_argument("--length", type=int, default=5000)
    args=parser.parse_args()
    return args
if __name__=="__main__":
    start_time = time.time()
    model_path = "/gpfs/data/johnsonslab/nlp-genomics/pasolli-2019/metagenomes_8192k.model"
    bpe = yttm.BPE(model=model_path)


    args = parse_args()
    idx = args.idx
    length = args.length

    df_path = '/gpfs/data/johnsonslab/nlp-genomics/almeida-2020/'
    df = pd.read_csv(os.path.join(df_path, 'genomes-all_metadata.tsv'), delimiter='\t',index_col=0)
    section = select_df(df, idx, length)
    # out_path = os.path.join(df_path, "tokenizations")
    tokenize_df(section, idx, bpe, df_path)
    print(time.time()-start_time)

    #take dataframe
    #get index argument from args
    #example: if index 0, idx = 0 * 5000
    # get df[idx: idx + 5000] or df[0:5000]
    #if index 1, idx = 1 * 5000
    #get df[idx:idx+5000] or df[5000:10000]
    #check that idx+5000 isn't longer than the dataframe
    #if it is, get df[idx:]

    #init tokenizer
    ###apply function:
    ##retrieve genome from gff
    ##tokenize
    #write new tsv with index written
