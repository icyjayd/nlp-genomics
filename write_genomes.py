import pandas as pd
import gzip
import re
import tarfile
import os
import youtokentome as yttm



def retrieve_genomes(path):
    with open(path, 'r') as f:
        file_content = f.readlines()
        file_content = [content.strip() for content in file_content]
    genomes = {}
    bases = ""
    header = file_content[0]
    for i in range(1, len(file_content)):
        if(">") in file_content[i]:
            genomes[header] = bases
            header = file_content[i]
            bases=""
        else:
            bases+= file_content[i]       
    
    return genomes

def write_genomes(folder, filename):
    with open(os.path.join(folder, filename), 'w') as f:
        for subfolder in os.listdir(folder):
            if('tar' in subfolder or 'txt' in subfolder):
                continue
            folder_path = os.path.join(folder, subfolder)
            for file in os.listdir(folder_path):
                path = os.path.join(folder_path, file)
                genomes = list(retrieve_genomes(path).values())
                for genome in genomes:
                    f.write(genome + '\n')

write_genomes('/gpfs/data/johnsonslab/nlp-genomics/pasolli-2019', 'all_genomes_unlabeled.txt')   

            
