import os
import numpy as np
import pandas as pd
import tables
from tables import *
path = '/gpfs/data/johnsonslab/nlp-genomics/almeida-2020'
all_tokens = set()
max_len = -np.inf
df = pd.read_csv(os.path.join(path, 'all_species_clades.csv'))
with open_file(os.path.join(path, "tokenizations_819k_poc_new.h5"), 'a') as h5file:
    data = h5file.root.data
    for i in range(len(df)):
        tokens = data['Tknz%d' % i].read()
        max_len = max(max_len, len(tokens))
        all_tokens.update(set(tokens))
        print(i, max_len)
    token_set = h5file.create_group('/', 'token_vocabulary', "Token Vocabulary")
    h5file.create_array("/token_vocabulary", 'vocab', list(all_tokens))
print("vocab size:", len(token_set))
print("all tokens accounted for")