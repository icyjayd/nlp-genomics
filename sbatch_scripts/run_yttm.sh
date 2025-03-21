#!/bin/bash
#
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --mem=120G
#SBATCH --time 14-00:00:00
#SBATCH --partition=cpu_long
#SBATCH --job-name bpe_metagenomes
#SBATCH --mail-type=END
#SBATCH --mail-user=juan.irizarry.cole@gmail.com

source activate /gpfs/home/jic286/.conda/envs/imblearn_env

python /gpfs/scratch/jic286/JohnsonLab/yttm_bpe.py