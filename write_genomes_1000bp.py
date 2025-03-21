with open('/gpfs/data/johnsonslab/nlp-genomics/pasolli-2019/all_genomes_unlabeled.txt', 'r') as f:
    with open('/gpfs/data/johnsonslab/nlp-genomics/pasolli-2019/all_genomes_unlabeled_1000bp.txt', 'w') as g:
        for line in f:
            genome = line.strip()
            for i in range(0, len(genome), 1000):
                stretch = genome[i:i+1000]
                g.write(stretch + '\n')