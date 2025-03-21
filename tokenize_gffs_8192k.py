import os
import pandas as pd
import youtokentome as yttm
from BCBio import GFF

def retrieve_genome_from_gff(in_file):
    with(open(in_file)) as in_handle:
        return "".join([str(rec.seq) for rec in GFF.parse(in_handle)])

model_path = "/gpfs/data/johnsonslab/nlp-genomics/pasolli-2019/metagenomes_8192k.model"
bpe = yttm.BPE(model=model_path)
path = '/gpfs/data/johnsonslab/nlp-genomics/almeida-2020/'
all_species = pd.read_csv(os.path.join(path, "all_species_clades.csv"), index_col=0)
tokenizations = []

for filename in all_species.index:
    seq = retrieve_genome_from_gff(os.path.join(path, 'gffs', filename))
    tokens = bpe.encode(seq)
    tokenizations.append(tokens)

tokenization_series = pd.Series(tokenizations_list, index=self.df.index)
all_species['tokens'] = tokenization_series
all_species.to_csv(os.path.join(self.path, 'all_species_clades_tokens_8192k.csv'))
