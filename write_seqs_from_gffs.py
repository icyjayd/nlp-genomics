import pandas as pd
import os
from BCBio import GFF


def retrieve_genome_from_genome_name(name):
    with(open(os.path.join('/gpfs/data/johnsonslab/nlp-genomics/almeida-2020/gffs/',name))) as in_handle:
        return "".join([str(rec.seq) for rec in GFF.parse(in_handle)])

def write_seq_from_gff(name, path):
    genome = retrieve_genome_from_genome_name(name)
    with (open(os.path.join(path, name +'.txt'), 'w' )) as f:
        f.write(genome)

if __name__=='__main__':
    path = '/gpfs/data/johnsonslab/nlp-genomics/almeida-2020/'
    files = sorted(os.listdir(os.path.join(path, 'gffs')), reverse=True)
#    df = pd.read_csv(os.path.join(path, 'genomes-all_metadata.tsv'), sep='\t', index_col=0)
    for i in range(17000, len(files)):
        write_seq_from_gff(files[i], os.path.join(path, 'genomes'))
