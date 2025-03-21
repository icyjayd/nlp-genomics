import numpy as np
np.random.seed(0)

with open('/gpfs/data/johnsonslab/nlp-genomics/pasolli-2019/all_genomes_unlabeled.txt', 'r') as m:
    for line in m:
        idx = np.random.randint(0, 1000)
        path = '/gpfs/data/johnsonslab/nlp-genomics/pasolli-2019/all_genomes_unlabeled_sample-0.1-{:0>3d}.txt'.format(idx)
        with open(path, 'a') as f:
            f.write(line)