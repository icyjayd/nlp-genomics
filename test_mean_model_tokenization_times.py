import time
import pandas as pd
import youtokentome as yttm
import os
import numpy as np
from BCBio import GFF

path = '/gpfs/data/johnsonslab/nlp-genomics/almeida-2020/'

df = pd.read_csv(os.path.join(path, 'all_species_clades.csv'), index_col=None)

def retrieve_genome_from_gff(in_file):
    with(open(in_file)) as in_handle:
        return "".join([str(rec.seq) for rec in GFF.parse(in_handle)])

model_list = ['metagenomes_8192.model', 'metagenomes_1000bp_8192.model', 'metagenomes_819k.model','metagenomes_8192k.model']
column_list = [model[model.find('_')+1:model.rfind('.')] for model in model_list]
trial_df = pd.DataFrame(index = column_list, columns = ['Mean tokenzation time (n=3000)'])
# trial_df = trial_df.set_index('Trial')
# trial_df.index.name = 'Trial'
sample_num =3000
samples = [retrieve_genome_from_gff(os.path.join(path, "gffs", x)) for x in df['file'].sample(n=sample_num)]
for i, model in enumerate(model_list):
    bpe = yttm.BPE(model=os.path.join("/gpfs/data/johnsonslab/nlp-genomics/pasolli-2019", model))
#     trial_means = []    
#     for j in range(num_trials):
#         sample = samples[j * sample_num: (j+1)* sample_num]
    start_time = time.time()
    for j in range(len(samples)):
        tokens = bpe.encode(samples[j])
    trial_mean = (time.time()-start_time)/len(samples)
    trial_df.iloc[i] = trial_mean
#     trial_means.append((time.time()-start_time)/len(samples))
#     trial_means = pd.Series(trial_means)
#     trial_df[column_list[i+1]] = trial_means
# means_of_means = []
# for column in trial_df.columns:
#     means_of_means.append(trial_df[column].mean())

# trial_df.loc[len(trial_df)] = means_of_means
# trial_df.index = list(np.arange(len(trial_df)))[:-1] + ['Mean'] 
# trial_df.index.name = 'Trial'
trial_df.to_csv(os.path.join(path, 'BPE_vocab_size_tokenization_speed_tests.csv'), index=True)
trial_df