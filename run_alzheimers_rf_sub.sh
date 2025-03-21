#!/bin/bash
#
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=100G
#SBATCH --time 7-00:00:00
#SBATCH --partition=cpu_medium
#SBATCH --job-name alz_rf
#SBATCH --mail-type=END
#SBATCH --mail-user=juan.irizarry.cole@gmail.com
#SBATCH --output=alzheimers_rf_output-%j.out
#SBATCH --error=alzheimers_rf_error-%j.out

source /gpfs/share/apps/anaconda3/cpu/5.3.1/etc/profile.d/conda.sh
conda activate /gpfs/home/jic286/.conda/envs/hyena-dna-new

python -u alzheimers_rf.py $SLURM_ARRAY_TASK_ID