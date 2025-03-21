#!/bin/bash
#
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --mem=20G
#SBATCH --time 14-00:00:00
#SBATCH --partition=cpu_long
#SBATCH --job-name write_seqs
#SBATCH --mail-type=END
#SBATCH --mail-user=juan.irizarry.cole@gmail.com

source activate /gpfs/home/jic286/.conda/envs/imblearn_env
python write_seqs_from_gffs.py