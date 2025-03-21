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

bash /gpfs/data/johnsonslab/nlp-genomics/alzheimers/ferreiro-2023/ena-file-download-read_run-PRJNA798058-fastq_ftp-20240501-1630.sh