#!/bin/bash
#
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=1400G
#SBATCH --time 5-00:00:00
#SBATCH --partition=fn_medium
#SBATCH --job-name bpe_metagenomes
#SBATCH --mail-type=END
#SBATCH --mail-user=juan.irizarry.cole@gmail.com

source activate /gpfs/home/jic286/.conda/envs/imblearn_env

yttm bpe --data /gpfs/data/johnsonslab/nlp-genomics/pasolli-2019/all_genomes_unlabeled_sample-A0.1-1.txt --model /gpfs/data/johnsonslab/nlp-genomics/pasolli-2019/metagenomes_819k.model --vocab_size 819200