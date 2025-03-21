#!/bin/bash


#SBATCH --partition=gpu8_medium
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=4
#SBATCH --time=1-00:00:00
#SBATCH --mem-per-cpu=128G
#SBATCH --gres=gpu:1
#SBATCH --job-name HF-test

#module load anaconda3/gpu/5.2.0
source activate ~/.conda/envs/py36
CUDA_LAUNCH_BLOCKING=1
python ~/JohnsonLab/nlp_main.py