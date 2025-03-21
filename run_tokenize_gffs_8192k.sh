#!/bin/bash
#
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --mem=1500G
#SBATCH --time 14-00:00:00
#SBATCH --partition=fn_long
#SBATCH --job-name tokenize_gffs
#SBATCH --mail-type=END
#SBATCH --mail-user=juan.irizarry.cole@gmail.com

source activate /gpfs/home/jic286/.conda/envs/imblearn_env

python /gpfs/scratch/jic286/JohnsonLab/tokenize_gffs_8192k.py