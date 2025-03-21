#!/bin/bash
#
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=40G
#SBATCH --time 28-00:00:00
#SBATCH --partition=cpu_long
#SBATCH --job-name bpe_time_test

source /gpfs/share/apps/anaconda3/cpu/5.3.1/etc/profile.d/conda.sh
conda activate /gpfs/home/jic286/.conda/envs/imblearn_env

python test_mean_model_tokenization_times.py
