#!/bin/bash
#
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=100G
#SBATCH --time 5-00:00:00
#SBATCH --partition=cpu_medium
#SBATCH --job-name alz_ml
#SBATCH --mail-type=END
#SBATCH --mail-user=juan.irizarry.cole@gmail.com
#SBATCH --output=alzheimers_ml_output-%j.out
#SBATCH --error=alzheimers_ml_error-%j.out

source /gpfs/share/apps/anaconda3/cpu/5.3.1/etc/profile.d/conda.sh
conda activate /gpfs/home/jic286/.conda/envs/hyena-dna-new

#python -u alzheimers_ml.py 16 lr --lr_penalty l2
#python -u alzheimers_ml.py 16 svm
#python -u alzheimers_ml.py 8 knn
python -u alzheimers_ml.py 100 rf --bpe_model /gpfs/data/johnsonslab/nlp-genomics/alzheimers/ferreiro-2023/kneaded_tokenizations_81920.h5
python -u alzheimers_ml.py 100 rf --bpe_model /gpfs/data/johnsonslab/nlp-genomics/alzheimers/ferreiro-2023/kneaded_tokenizations_8192.h5
python -u alzheimers_ml.py 100 rf --bpe_model /gpfs/data/johnsonslab/nlp-genomics/alzheimers/ferreiro-2023/raw_tokenizations_8192k.h5
python -u alzheimers_ml.py 100 rf --bpe_model /gpfs/data/johnsonslab/nlp-genomics/alzheimers/ferreiro-2023/raw_tokenizations_819k.h5
python -u alzheimers_ml.py 100 rf --bpe_model /gpfs/data/johnsonslab/nlp-genomics/alzheimers/ferreiro-2023/raw_tokenizations_81920.h5
python -u alzheimers_ml.py 100 rf --bpe_model /gpfs/data/johnsonslab/nlp-genomics/alzheimers/ferreiro-2023/raw_tokenizations_8192.h5
