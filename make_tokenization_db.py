import sqlite3
import pandas as pd
import os
import sys
from BCBio import GFF
import youtokentome as yttm
model_path = "/gpfs/data/johnsonslab/nlp-genomics/pasolli-2019/metagenomes_1000bp_8192.model" ###MAKE SURE MODEL PATH IS CORRECT
bpe = yttm.BPE(model=model_path)
path = '/gpfs/data/johnsonslab/nlp-genomics/almeida-2020'

df = pd.read_csv(os.path.join(path, 'all_species_clades.csv'))

def retrieve_genome_from_genome_name(name):
    with(open(os.path.join('/gpfs/data/johnsonslab/nlp-genomics/almeida-2020/gffs/',name + '.gff'))) as in_handle:
        return "".join([str(rec.seq) for rec in GFF.parse(in_handle)])

##if missing entries, check 1600-1602
#starting 819k from 140148 - NOT ACTUALLY STARTED, MAKE SURE MODEL PATH IS CORRECT
#starting 1000bp_8192 from 154377
#if need to restart 8192k DON'T FORGET TO CHANGE THE START INDEX
with sqlite3.connect(os.path.join(path, 'tokenizations_db_819k_poc.db')) as conn:
    for i in range(140148, len(df)):
        row = df.iloc[[i]]
        genome = retrieve_genome_from_genome_name(row['file'].iloc[0][:-4])
        tokens = bpe.encode(genome)
        row['tokenization'] = repr(tokens)
        row.to_sql('data', con=conn, if_exists='append', index=False)
        print(i)
    