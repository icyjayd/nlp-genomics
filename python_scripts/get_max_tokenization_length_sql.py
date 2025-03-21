import numpy as np
import sqlite3
import os
import pandas as pd

path = '/gpfs/data/johnsonslab/nlp-genomics/almeida-2020'

max_len = -np.inf
with sqlite3.connect(os.path.join(path, 'tokenizations_db_8192k_poc.db')) as conn:
    dfs = pd.read_sql('SELECT * from data', conn, chunksize=10)
    for i, df in enumerate(dfs):
        for tokenization in df['tokenization']:
            tokens = eval(tokenization)
            max_len = max(max_len, len(tokens))
            print(max_len)