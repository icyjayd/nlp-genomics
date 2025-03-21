#!/bin/bash
#

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --mem=20G
#SBATCH --time 7-00:00:00
#SBATCH --partition=cpu_medium
#SBATCH --job-name sample_details
#SBATCH --mail-type=END
#SBATCH --mail-user=juan.irizarry.cole@gmail.com

source activate /gpfs/home/jic286/.conda/envs/imblearn_env

python /gpfs/home/jic286/jic286/JohnsonLab/get_share_counts.py