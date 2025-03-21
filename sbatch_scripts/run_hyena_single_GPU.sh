#!/bin/bash

#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=4
#SBATCH --time=28-00:00:00
#SBATCH --mem-per-cpu=16G
#SBATCH --gres=gpu:a100:1
#SBATCH --job-name hyena-single
#SBATCH --mail-type=ALL
#SBATCH --mail-user=juan.irizarry.cole@gmail.com
#SBATCH --output=hyena_single_output-%j
#SBATCH --error=hyena_single_error-%j

source /gpfs/share/apps/anaconda3/cpu/5.3.1/etc/profile.d/conda.sh
conda deactivate
conda activate /gpfs/home/jic286/.conda/envs/hyena-dna-new

python -u hyena_dna_custom_single_GPU.py

#slurm-32563924.out