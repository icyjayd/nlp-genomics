#!/bin/bash
#
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --mem=20G
#SBATCH --time 14-00:00:00
#SBATCH --partition=cpu_long
#SBATCH --job-name sample_genomes_1000
#SBATCH --mail-type=END
#SBATCH --mail-user=juan.irizarry.cole@gmail.com

source activate /gpfs/home/jic286/.conda/envs/imblearn_env
python sample_genomes_1000.py