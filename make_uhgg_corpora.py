import pandas as pd
import random
from BCBio import GFF
import os
import sys

path = '/gpfs/data/johnsonslab/nlp-genomics/almeida-2020'

df = pd.read_csv(os.path.join(path, 'genomes-all_metadata.tsv'), sep='\t', index_col=0)

def retrieve_genome_from_genome_name(name):
    with(open(os.path.join('/gpfs/data/johnsonslab/nlp-genomics/almeida-2020/gffs/', name+ '.gff'))) as in_handle:
        return "".join([str(rec.seq) for rec in GFF.parse(in_handle)])

filename = 'corpora/uhgg_all_genomes_ordered'
filepath = os.path.join(path,filename + '.txt' )
with(open(filepath, 'a+')) as f:
    for i in range(len(df.index)):
        name = df.index[i]
        genome = retrieve_genome_from_genome_name(name)
        f.write(genome + "\n")
        sample_num = random.randint(0, 500)
        sample_filepath = os.path.join(path, filename + "_sample_" + str(sample_num) + '.txt')
        with open(sample_filepath, 'a+') as g:
            g.write(genome + "\n")
        print(i, flush=True)