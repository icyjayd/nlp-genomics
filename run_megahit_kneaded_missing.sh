#!/bin/bash
#
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --mem=1000G
#SBATCH --time 28-00:00:00
#SBATCH --partition=fn_long
#SBATCH --job-name megahit
#SBATCH --mail-type=END
#SBATCH --mail-user=juan.irizarry.cole@gmail.com

source /gpfs/share/apps/anaconda3/cpu/5.3.1/etc/profile.d/conda.sh
conda activate /gpfs/home/jic286/.conda/envs/humann2
bash /gpfs/scratch/jic286/JohnsonLab/megahit_kneaded_missing.sh
