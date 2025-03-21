#!/bin/bash
#
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --mem=8G
#SBATCH --time 1-00:00:00
#SBATCH --partition=cpu_medium
#SBATCH --job-name generate_file
#SBATCH --mail-type=END
#SBATCH --mail-user=juan.irizarry.cole@gmail.com

#bash /gpfs/scratch/jic286/JohnsonLab/get_corrupted_ferreiro_metagenomes.sh
#wget -nc ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR176/065/SRR17648365/SRR17648365_1.fastq.gz
#wget -nc ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR176/075/SRR17648375/SRR17648375_2.fastq.gz
#wget -nc ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR176/001/SRR17648401/SRR17648401_2.fastq.gz
wget -nc ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR176/005/SRR17648405/SRR17648405_2.fastq.gz
#wget -nc ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR176/008/SRR17648408/SRR17648408_1.fastq.gz
#wget -nc ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR176/015/SRR17648415/SRR17648415_1.fastq.gz
#wget -nc ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR176/037/SRR17648437/SRR17648437_2.fastq.gz
#wget -nc ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR176/039/SRR17648439/SRR17648439_2.fastq.gz
