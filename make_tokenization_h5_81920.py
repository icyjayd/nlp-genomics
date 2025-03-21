import os
import numpy as np
import pandas as pd
from tables import *
import youtokentome as yttm
from BCBio import GFF
path = '/gpfs/data/johnsonslab/nlp-genomics/almeida-2020'

df = pd.read_csv(os.path.join(path, 'all_species_clades.csv'))

def retrieve_genome_from_genome_name(name):
    with(open(os.path.join('/gpfs/data/johnsonslab/nlp-genomics/almeida-2020/gffs/',name + '.gff'))) as in_handle:
        return "".join([str(rec.seq) for rec in GFF.parse(in_handle)])
model_path = "/gpfs/data/johnsonslab/nlp-genomics/pasolli-2019/metagenomes_81920.model"

bpe = yttm.BPE(model=model_path)

with open_file(os.path.join(path, "tokenizations_81920_poc.h5"), 'w') as h5file:
    group = h5file.create_group('/', "data", "Tokenization Data")
    for i in range(len(df)):
        genome = retrieve_genome_from_genome_name(df['file'][i][:-4])
        tokens = bpe.encode(genome)
        h5file.create_array("/data", 'Tknz%d'% i, tokens)
        print(i, tokens[:3])
