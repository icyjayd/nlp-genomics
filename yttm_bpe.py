import random

import youtokentome as yttm

train_data_path = "/gpfs/data/johnsonslab/nlp-genomics/pasolli-2019/all_genomes_unlabeled.txt"
model_path = "/gpfs/data/johnsonslab/nlp-genomics/pasolli-2019/metagenomes.model"

yttm.BPE.train(data=train_data_path, vocab_size=5000, model=model_path)
