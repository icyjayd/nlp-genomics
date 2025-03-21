#!/bin/bash


#SBATCH --partition=gpu8_long
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=4
#SBATCH --time=7-00:00:00
#SBATCH --mem-per-cpu=16G
#SBATCH --gres=gpu:1
#SBATCH --job-name gnet_conv
#SBATCH --output=run_gnet_conv.out

#conda init bash

module load anaconda3/gpu/5.2.0-cuda10.1
module load cuda/10.1.105

conda activate ~/.conda/envs/py36

python genomenet_conv.py