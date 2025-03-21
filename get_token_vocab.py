import os
import numpy as np
import pandas as pd
import tables
from tables import *
path = '/gpfs/data/johnsonslab/nlp-genomics/almeida-2020'
all_tokens = set()
df = pd.read_csv(os.path.join(path, 'all_species_clades.csv'))
with open_file(os.path.join(path, "tokenizations_8192k_poc.h5"), 'a') as h5file:
    data = h5file.root.data
    for i in range(len(df)):
        tokens = data['Tknz%d' % i].read()
        all_tokens.update(set(tokens))
        print(i, len(all_tokens))
    token_set = h5file.create_group('/', 'token_vocabulary', "Token Vocabulary")
    h5file.create_array("/token_vocabulary", 'vocab', list(all_tokens))