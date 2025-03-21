import pandas as pd
from sklearn.model_selection import train_test_split
import pandas as pd
import datetime
import math
import torch
import torch.nn as nn
from tqdm import tqdm

import numpy as np
from sklearn.model_selection import train_test_split
from os import listdir
%cd E:\Documents\Johnson Lab\mimic
chart = pd.read_csv('CHARTEVENTS.csv.gz', compression='gzip', header=0, sep=',', quotechar='"',low_memory=False)

ts = datetime.datetime.now().timestamp()
chunksize = 10**6
chunks = []
for chunk in pd.read_csv('CHARTEVENTS.csv.gz', compression='gzip', header=0, sep=',', quotechar='"', chunksize=chunksize, low_memory=False):
    chunks.append(chunk)
te = datetime.datetime.now().timestamp()
t = te-ts
print("Operation complete in {} seconds.".format(t))
notes = pd.concat(chunks)
notes.to_csv(r'notetext2.csv.gz',compression='gzip')
diag = pd.read_csv('D_ICD_DIAGNOSES.csv.gz', compression = 'gzip')
len(diag['LONG_TITLE'].unique())
len(diag['SHORT_TITLE'].unique())
len(diag['ICD9_CODE'].unique())
cpt = pd.read_csv('CPTEVENTS.csv.gz', compression='gzip', encoding='utf-8' )
cpt = cpt.loc[cpt['DESCRIPTION'].notnull()]
desc = cpt['DESCRIPTION']
procs = pd.read_csv('D_ICD_PROCEDURES.csv.gz', compression='gzip', encoding='utf-8')
len(procs['SHORT_TITLE'].unique())
len(procs['LONG_TITLE'].unique())
len(desc.unique())
chartevents = pd.read_csv('CHARTEVENTS.csv.gz', compression='gzip', nrows=100000, encoding='utf-8' )

inpevents = pd.read_csv('INPUTEVENTS_MV.csv.gz', compression ='gzip', encoding='utf-8', nrows=100000)
len(inpevents['ORDERCATEGORYNAME'].unique())
callout = pd.read_csv('CALLOUT.csv.gz', compression = 'gzip', encoding='utf-8')

micro = pd.read_csv('MICROBIOLOGYEVENTS.csv.gz', compression='gzip', encoding='utf-8')

test = pd.read_csv('NOTEEVENTS.csv.gz', compression='gzip', header=0, sep=',', quotechar='"',low_memory=False)
test['TEXT'].to_csv(r'notetext.txt', index = False, header=False, sep=' ')

test = notes.values
test = str(test)
#diag =0
#micro = 1
#desc = 2
#procs = 3