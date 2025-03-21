#!/bin/bash
#
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --mem=60G
#SBATCH --time 5-00:00:00
#SBATCH --partition=cpu_medium
#SBATCH --job-name all_genomes

source activate /gpfs/home/jic286/.conda/envs/imblearn_env

python /gpfs/scratch/jic286/JohnsonLab/write_genomes_1000bp.py

echo "all genomes written"