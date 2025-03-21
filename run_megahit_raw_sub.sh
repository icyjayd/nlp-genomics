#!/bin/bash
#
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --mem=20G
#SBATCH --time 28-00:00:00
#SBATCH --partition=cpu_long
#SBATCH --job-name megahit
#SBATCH --mail-type=END
#SBATCH --mail-user=juan.irizarry.cole@gmail.com
#SBATCH --output=megahit_t2d_raw-out-%j.out
#SBATCH --error=megahit_t2d_raw-error-%j.out

source /gpfs/share/apps/anaconda3/cpu/5.3.1/etc/profile.d/conda.sh
conda activate /gpfs/home/jic286/.conda/envs/humann2
bash /gpfs/scratch/jic286/JohnsonLab/megahit_raw_t2d_$SLURM_ARRAY_TASK_ID.sh