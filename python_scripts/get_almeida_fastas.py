import os
import ftplib
destination  = '/gpfs/data/johnsonslab/nlp-genomics/almeida-2020/fastas'
os.chdir(destination)
ftp = ftplib.FTP("ftp.ebi.ac.uk")
ftp.login("anonymous", "foo")
path = '/pub/databases/metagenomics/mgnify_genomes/human-gut/v2.0/species_catalogue'
# '/pub/databases/metagenomics/mgnify_genomes/human-gut/v2.0/species_catalogue/MGYG0000000/MGYG000000001/genome'
ftp.cwd(path)
folders = ftp.nlst()
for folder in folders:
    ftp.cwd(folder)#changes to /num7zeroes
    subfolders = ftp.nlst()
    for subfolder in subfolders:
        ftp.cwd(os.path.join(subfolder, "genome"))
        files = ftp.nlst()
        for file in files:
            if ".fna" in file and '.fai' not in file:
                with open(os.path.join(destination,file),"wb") as f:
                    ftp.retrbinary("RETR "+file, f.write)
        ftp.cwd('../..')
    ftp.cwd(path)

        
ftp.close()
