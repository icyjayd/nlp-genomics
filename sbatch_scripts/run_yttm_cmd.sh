#!/bin/bash
#
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=100G
#SBATCH --time 28-00:00:00
#SBATCH --partition=fn_long
#SBATCH --job-name yttm_cmd
#SBATCH --mail-type=END
#SBATCH --mail-user=juan.irizarry.cole@gmail.com

source /gpfs/share/apps/anaconda3/cpu/5.3.1/etc/profile.d/conda.sh
conda activate /gpfs/home/jic286/.conda/envs/hyena-dna-new
#yttm bpe --data /gpfs/data/johnsonslab/nlp-genomics/almeida-2020/corpora/test100k.txt --model /gpfs/data/johnsonslab/nlp-genomics/almeida-2020/yttm_models/test100k.model --vocab_size 8192000

#pasolli
#yttm bpe --data /gpfs/data/johnsonslab/nlp-genomics/pasolli-2019/sample-A0.1-1-6k.txt --model /gpfs/data/johnsonslab/nlp-genomics/pasolli-2019/metagenome_brown_sample_8192k.model --vocab_size 8192000
#yttm bpe --data /gpfs/data/johnsonslab/nlp-genomics/pasolli-2019/sample-A0.1-1-6k.txt --model /gpfs/data/johnsonslab/nlp-genomics/pasolli-2019/metagenome_brown_sample_819k.model --vocab_size 819200
#yttm bpe --data /gpfs/data/johnsonslab/nlp-genomics/pasolli-2019/sample-A0.1-1-6k.txt --model /gpfs/data/johnsonslab/nlp-genomics/pasolli-2019/metagenome_brown_sample_81k.model --vocab_size 81920
#yttm bpe --data /gpfs/data/johnsonslab/nlp-genomics/pasolli-2019/sample-A0.1-1-6k.txt --model /gpfs/data/johnsonslab/nlp-genomics/pasolli-2019/metagenome_brown_sample_8k.model --vocab_size 8192

#VFDB
#yttm bpe --data /gpfs/data/johnsonslab/nlp-genomics/VFDB/VFDB_1_seq_per_line.txt --model /gpfs/data/johnsonslab/nlp-genomics/VFDB/VFDB_8192k.model --vocab_size 8192000
#yttm bpe --data /gpfs/data/johnsonslab/nlp-genomics/VFDB/VFDB_1_seq_per_line.txt --model /gpfs/data/johnsonslab/nlp-genomics/VFDB/VFDB_819k.model --vocab_size 819200
#yttm bpe --data /gpfs/data/johnsonslab/nlp-genomics/VFDB/VFDB_1_seq_per_line.txt --model /gpfs/data/johnsonslab/nlp-genomics/VFDB/VFDB_81k.model --vocab_size 81920
#yttm bpe --data /gpfs/data/johnsonslab/nlp-genomics/VFDB/VFDB_1_seq_per_line.txt --model /gpfs/data/johnsonslab/nlp-genomics/VFDB/VFDB_8k.model --vocab_size 8192

#T2D
yttm bpe --data /gpfs/data/johnsonslab/nlp-genomics/t2d/corpus_chunks/raw/t2d_raw_chunk_0.txt --model /gpfs/data/johnsonslab/nlp-genomics/t2d/T2D_raw_8192k.model --vocab_size 8192000