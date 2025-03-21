#!/bin/bash
#
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=20G
#SBATCH --time 5-00:00:00
#SBATCH --partition=fn_medium
#SBATCH --job-name 8192k_nr0
#SBATCH --mail-type=END
#SBATCH --mail-user=juan.irizarry.cole@gmail.com

source activate /gpfs/home/jic286/.conda/envs/imblearn_env

yttm bpe --data /gpfs/data/johnsonslab/nlp-genomics/almeida-2020/corpora/test100k.txt --model /gpfs/data/johnsonslab/nlp-genomics/almeida-2020/yttm_models/test100k.model --vocab_size 8192000