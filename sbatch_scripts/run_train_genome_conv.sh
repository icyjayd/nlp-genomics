#!/bin/bash

#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=4
#SBATCH --time=28-00:00:00
#SBATCH --mem-per-cpu=20G
#SBATCH --gres=gpu:a100:1
#SBATCH --job-name genome_conv

source /gpfs/share/apps/anaconda3/cpu/5.3.1/etc/profile.d/conda.sh
conda deactivate
conda activate /gpfs/home/jic286/.conda/envs/new_new_torch

python -u train_genome_conv.py > train_genome_conv_8192k_10-27-23.out

