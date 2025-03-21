#!/bin/bash
#
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --mem=20G
#SBATCH --time 28-00:00:00
#SBATCH --partition=cpu_long
#SBATCH --job-name transfer_s2h
#SBATCH --mail-type=END
#SBATCH --mail-user=juan.irizarry.cole@gmail.com

conda init bash
conda activate ~/.conda/envs/py36
python -u transfer_sqlite_to_hdf5.py > sqlite2hdf5.out