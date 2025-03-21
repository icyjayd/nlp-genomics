#!/bin/bash
#
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=20G
#SBATCH --time 5-00:00:00
#SBATCH --partition=cpu_medium
#SBATCH --job-name bpe_metagenomes
#SBATCH --mail-type=END
#SBATCH --mail-user=juan.irizarry.cole@gmail.com
#SBATCH --output=yttm_brown-%j.out
#SBATCH --error=yttm_brown-%j.out

source /gpfs/share/apps/anaconda3/cpu/5.3.1/etc/profile.d/conda.sh
conda activate /gpfs/home/jic286/.conda/envs/hyena-dna-new
yttm bpe --data /gpfs/data/johnsonslab/nlp-genomics/english_corpora/brown_nowhitelines.txt --model /gpfs/data/johnsonslab/nlp-genomics/english_corpora/brown_8192k.model --vocab_size 8192000
yttm bpe --data /gpfs/data/johnsonslab/nlp-genomics/english_corpora/brown_nowhitelines.txt --model /gpfs/data/johnsonslab/nlp-genomics/english_corpora/brown_819k.model --vocab_size 819200
yttm bpe --data /gpfs/data/johnsonslab/nlp-genomics/english_corpora/brown_nowhitelines.txt --model /gpfs/data/johnsonslab/nlp-genomics/english_corpora/brown_81k.model --vocab_size 81920
yttm bpe --data /gpfs/data/johnsonslab/nlp-genomics/english_corpora/brown_nowhitelines.txt --model /gpfs/data/johnsonslab/nlp-genomics/english_corpora/brown_8k.model --vocab_size 8192
