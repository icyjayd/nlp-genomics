import numpy as np
np.random.seed(0)

with open('/gpfs/data/johnsonslab/nlp-genomics/pasolli-2019/all_genomes_unlabeled.txt', 'r') as inp:
    with open('/gpfs/data/johnsonslab/nlp-genomics/pasolli-2019/all_genomes_unlabeled_sample-0.5.txt', 'w') as out:
        for line in inp:
            if(np.random.rand()>=0.995):
                out.write(line)