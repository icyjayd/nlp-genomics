#!/bin/bash
#
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=40G
#SBATCH --time 5-00:00:00
#SBATCH --partition=fn_medium
#SBATCH --job-name t2d_mr
#SBATCH --mail-type=END
#SBATCH --mail-user=juan.irizarry.cole@gmail.com
#SBATCH --output=t2d_ml_output-%j.out
#SBATCH --error=t2d_ml_error-%j.out

source /gpfs/share/apps/anaconda3/cpu/5.3.1/etc/profile.d/conda.sh
conda activate /gpfs/home/jic286/.conda/envs/hyena-dna-new

#python -u t2d_ml.py 0 xgboost
#python -u t2d_ml.py 100 svm
#python -u t2d_ml.py 100 lr
#python -u t2d_ml.py 100 lr
#python -u t2d_ml.py 0 lr
#python -u t2d_ml.py 0 lr --lr_max_iters 200
#python -u t2d_ml.py 0 lr --lr_max_iters 200
python -u t2d_ml.py 100 rf
#python -u t2d_ml.py 0 knn
#python -u t2d_ml.py 1000 xgboost
