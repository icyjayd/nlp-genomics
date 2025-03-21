#!/bin/bash
#
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --mem=20G
#SBATCH --time 1-00:00:00
#SBATCH --partition=cpu_medium
#SBATCH --job-name generate_file
SBATCH --mail-type=END
#SBATCH --mail-user=juan.irizarry.cole@gmail.com

source activate /gpfs/home/jic286/.conda/envs/imblearn_env
python generate_big_file.py