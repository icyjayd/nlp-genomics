#!/bin/bash
#
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --mem=20G
#SBATCH --time 1-00:00:00
#SBATCH --partition=cpu_medium
#SBATCH --job-name pretokenizing_uhgg
#SBATCH --mail-type=END
#SBATCH --mail-user=juan.irizarry.cole@gmail.com

source activate /gpfs/home/jic286/.conda/envs/imblearn_env
printf -v j "%03d" $SLURM_ARRAY_TASK_ID
python tokenize_uhgg_segment.py $j --length 50