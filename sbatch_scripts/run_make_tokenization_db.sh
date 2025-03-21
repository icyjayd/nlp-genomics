#!/bin/bash
#
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --mem=20G
#SBATCH --time 28-00:00:00
#SBATCH --partition=cpu_long
#SBATCH --job-name 1000bp_8192_make_db
#SBATCH --mail-type=END
#SBATCH --mail-user=juan.irizarry.cole@gmail.com

source activate /gpfs/home/jic286/.conda/envs/imblearn_env
python -u make_tokenization_db.py > mktknz_1000bp_8192.out