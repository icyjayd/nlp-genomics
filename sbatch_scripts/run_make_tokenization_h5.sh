#!/bin/bash
#
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --mem=20G
#SBATCH --time 28-00:00:00
#SBATCH --partition=cpu_long
#SBATCH --job-name 819k_h5
#SBATCH --mail-type=END
#SBATCH --mail-user=juan.irizarry.cole@gmail.com

conda init bash
conda activate ~/.conda/envs/py36
python -u make_tokenization_h5.py > mktknz_819k_h5_contd.out
