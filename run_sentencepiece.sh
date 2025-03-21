#!/bin/bash
#
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=200G
#SBATCH --time 5-00:00:00
#SBATCH --partition=cpu_medium
#SBATCH --job-name jupyter-notebook

source /gpfs/share/apps/anaconda3/cpu/5.3.1/etc/profile.d/conda.sh
conda activate /gpfs/home/jic286/.conda/envs/imblearn_env

#inp = $1
#model = $2
#vocab = $3
#pad = $4

#python train_sentencepiece.py -input $1 -model_prefix $2 -vocab_size $3 --pad_id $4
 python train_sentencepiece.py /gpfs/data/johnsonslab/nlp-genomics/pasolli-2019/all_genomes_unlabeled_1000bp.txt sp_1000bp_full 8192 --pad_id 3