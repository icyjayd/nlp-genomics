#!/bin/bash

#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=2
#SBATCH --time=28-00:00:00
#SBATCH --mem-per-cpu=120G
#SBATCH --gres=gpu:a100:4
#SBATCH --job-name hyena-multi
#SBATCH --mail-type=ALL
#SBATCH --mail-user=juan.irizarry.cole@gmail.com
#SBATCH --output=hyena_multi_test_output-%j
#SBATCH --error=hyena_multi_test_error-%j

source /gpfs/share/apps/anaconda3/cpu/5.3.1/etc/profile.d/conda.sh
#module load anaconda3/cpu/5.3.1
conda deactivate
conda activate /gpfs/home/jic286/.conda/envs/hyena-dna-new

python -u hyena_dna_custom_FSDP.py

#slurm-32563924.out