#!/bin/bash
#
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=20G
#SBATCH --time 28-00:00:00
#SBATCH --partition=cpu_long
#SBATCH --job-name bpe_custom
#SBATCH --mail-type=END
#SBATCH --mail-user=juan.irizarry.cole@gmail.com
#SBATCH --output=bpe_custom_output-%j.out
#SBATCH --error=bpe_custom_error-%j.out

source /gpfs/share/apps/anaconda3/cpu/5.3.1/etc/profile.d/conda.sh
conda activate /gpfs/home/jic286/.conda/envs/hyena-dna-new

#python -u bpe_with_whitespace.py 8192 /gpfs/data/johnsonslab/nlp-genomics/english_corpora/brown_nowhitelines.txt /gpfs/data/johnsonslab/nlp-genomics/english_corpora/brown_custom
#python -u bpe_with_whitespace.py 81920 /gpfs/data/johnsonslab/nlp-genomics/english_corpora/brown_nowhitelines.txt /gpfs/data/johnsonslab/nlp-genomics/english_corpora/brown_custom
#python -u bpe_with_whitespace.py 819200 /gpfs/data/johnsonslab/nlp-genomics/english_corpora/brown_nowhitelines.txt /gpfs/data/johnsonslab/nlp-genomics/english_corpora/brown_custom
python -u bpe_with_whitespace.py 8192000 /gpfs/data/johnsonslab/nlp-genomics/english_corpora/brown_nowhitelines.txt /gpfs/data/johnsonslab/nlp-genomics/english_corpora/brown_custom
