#!/bin/bash
#
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --mem=100G
#SBATCH --time 28-00:00:00
#SBATCH --partition=fn_long
#SBATCH --job-name tknz_db
#SBATCH --mail-type=END
#SBATCH --mail-user=juan.irizarry.cole@gmail.com

source /gpfs/share/apps/anaconda3/cpu/5.3.1/etc/profile.d/conda.sh
conda activate /gpfs/home/jic286/.conda/envs/hyena-dna-new
#python make_alzheimer_tknz_db.py
#python make_alz_tokenization_database.py 819k
#python make_alz_tokenization_database.py 81920
python make_alz_tokenization_database.py 8192

