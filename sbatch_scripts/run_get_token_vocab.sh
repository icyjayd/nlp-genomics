#!/bin/bash
#
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --mem=20G
#SBATCH --time 28-00:00:00
#SBATCH --partition=cpu_long
#SBATCH --job-name 8192k_vocab
#SBATCH --mail-type=END
#SBATCH --mail-user=juan.irizarry.cole@gmail.com

conda init bash
conda activate ~/.conda/envs/py36

python -u get_token_vocab.py

#slurm-25948398.out for 8192k