###This is the one that works
from contextlib import closing
from urllib.request import urlopen
import gzip
import pandas as pd
import os
from multiprocessing import cpu_count, Pool
path ='/gpfs/data/johnsonslab/nlp-genomics/almeida-2020/'
os.chdir(path)
df = pd.read_csv(os.path.join(path, 'genomes-all_metadata.tsv'), sep='\t')
for i in range(94460, 289233):

    url = df['FTP_download'][i]
    target_path = url[url.rfind('/')+1:-3]
    connected= False
    while not connected:
        try:
            with closing(urlopen(url)) as source:
                with gzip.open(source) as f:
                    with open(os.path.join('gffs',target_path), 'wb') as target:
                        target.write((f.read()))
                        connected=True
        except:
            connected=False
# print("All content downloaded")
#def download_gff(url):
#    target_path = url[url.rfind('/')+1:-3]
#    connected= False
#    while not connected:
#        try:
#            with closing(urlopen(url)) as source:
#                with gzip.open(source) as f:
#                    with open(os.path.join('gffs',target_path), 'wb') as target:
#                        target.write((f.read()))
#                        connected=True
        except:
            connected=False
#def pool_handler(df):
#    p = Pool(40)
#    p.map(download_gff, df['FTP_download'][94478:])

#if __name__=="__main__":
#    path ='/gpfs/data/johnsonslab/nlp-genomics/almeida-2020/'
#    os.chdir(path)
#    df = pd.read_csv(os.path.join(path, 'genomes-all_metadata.tsv'), sep='\t')
#    pool_handler(df)
#    print("All content downloaded")


