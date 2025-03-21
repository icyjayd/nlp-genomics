import sqlite3
import os
import numpy as np
import pandas as pd
from tables import *
# h5file.close()

path = '/gpfs/data/johnsonslab/nlp-genomics/almeida-2020/'
df = pd.read_csv(os.path.join(path, "all_species_clades.csv"))
with sqlite3.connect(os.path.join(path, 'tokenizations_db_8192k_poc.db')) as conn:
    with(open_file(os.path.join(path, 'tokenizations_8192k_poc.h5'),'w')) as h5file:

        group = h5file.create_group('/', "data", "Tokenization Data")
        cursor = conn.cursor()

        for i in range(len(df)):
            query = "SELECT tokenization FROM data WHERE rowid=%d" % (i + 1)
            res = (cursor.execute(query)).fetchall()[0]
            x = eval(res[0])

            h5file.create_array("/data", 'Tknz%d'% i, x)
            print(i, x[:3])
print("All tokenizations transferred")