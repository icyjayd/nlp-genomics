#!/bin/bash
#
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --mem=40G
#SBATCH --time 28-00:00:00
#SBATCH --partition=cpu_long
#SBATCH --job-name knead
#SBATCH --mail-type=END
#SBATCH --mail-user=juan.irizarry.cole@gmail.com
#SBATCH --output=knead_t2d-out-%j.out
#SBATCH --error=knead_t2d-error-%j.out

module load trimmomatic
source /gpfs/share/apps/anaconda3/cpu/5.3.1/etc/profile.d/conda.sh
conda activate /gpfs/home/jic286/.conda/envs/hyena-dna-new
bash /gpfs/scratch/jic286/JohnsonLab/remove_human_reads_t2d_$SLURM_ARRAY_TASK_ID.sh
#bash /gpfs/scratch/jic286/JohnsonLab/remove_human_reads_t2d_missing_$SLURM_ARRAY_TASK_ID.sh
