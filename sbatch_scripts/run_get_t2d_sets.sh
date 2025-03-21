#!/bin/bash
#
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --mem=20G
#SBATCH --time 28-00:00:00
#SBATCH --partition=cpu_long
#SBATCH --job-name get_t2d
#SBATCH --mail-type=END
#SBATCH --mail-user=juan.irizarry.cole@gmail.com
#SBATCH --output=get_t2d-out-%j.out
#SBATCH --error=get_t2d-error-%j.out

module load sratoolkit
echo $SLURM_ARRAY_TASK_ID
bash /gpfs/data/johnsonslab/nlp-genomics/t2d/dl_scripts/t2dfdumpfastqs$SLURM_ARRAY_TASK_ID.sh
#bash /gpfs/data/johnsonslab/nlp-genomics/t2d/dl_scripts/t2dfdump$SLURM_ARRAY_TASK_ID.sh
