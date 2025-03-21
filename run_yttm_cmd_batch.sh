#!/bin/bash
#
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --mem=280G
#SBATCH --time 05:00:00
#SBATCH --partition=cpu_short
#SBATCH --job-name bpe_metagenomes
#SBATCH --mail-type=END
#SBATCH --mail-user=juan.irizarry.cole@gmail.com

source activate /gpfs/home/jic286/.conda/envs/imblearn_env
printf -v j "%03d" $SLURM_ARRAY_TASK_ID
yttm bpe --data /gpfs/data/johnsonslab/nlp-genomics/pasolli-2019/all_genomes_unlabeled_sample-0.1-$j.txt --model /gpfs/data/johnsonslab/nlp-genomics/pasolli-2019/metagenomes_8192k_0.1s-$j.model --vocab_size 8192000