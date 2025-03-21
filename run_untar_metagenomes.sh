#!/bin/bash
#
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --mem=120G
#SBATCH --time 2-00:00:00
#SBATCH --partition=cpu_medium
#SBATCH --job-name metagenomes

source activate ~/.conda/envs/py36
python /gpfs/home/jic286/JohnsonLab/untar_metagenomes.py