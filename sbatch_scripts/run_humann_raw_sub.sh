#!/bin/bash
#
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=40G
#SBATCH --time 28-00:00:00
#SBATCH --partition=fn_long
#SBATCH --job-name humann
#SBATCH --mail-type=END
#SBATCH --mail-user=juan.irizarry.cole@gmail.com
#SBATCH --output=humann_t2d_raw-out-%j.out
#SBATCH --error=humann_t2d_raw-error-%j.out

source /gpfs/share/apps/anaconda3/cpu/5.3.1/etc/profile.d/conda.sh
conda deactivate
conda activate /gpfs/home/jic286/.conda/envs/mpa

#module load metaphlan2/097a52362c79
#module load diamond/0.9.18
#module load bowtie2/2.5.3
bash /gpfs/scratch/jic286/JohnsonLab/humann_raw_t2d_$SLURM_ARRAY_TASK_ID.sh
#humann -i /gpfs/data/johnsonslab/nlp-genomics/t2d/SRR341706_1.fasta -o /gpfs/data/johnsonslab/nlp-genomics/t2d/T2D1.as2.NLM031/humann_raw_out
#/gpfs/home/jic286/.conda/envs/mpa/bin/metaphlan /gpfs/data/johnsonslab/nlp-genomics/t2d/T2D1.as2.NLM031/humann_raw_out/SRR341706_1_humann_temp/tmpy2ctxhj8/tmpbbrwjh6q -t rel_ab -o /gpfs/data/johnsonslab/nlp-genomics/t2d/T2D1.as2.NLM031/humann_raw_out/SRR341706_1_humann_temp/SRR341706_1_metaphlan_bugs_list.tsv --input_type fasta --bowtie2out /gpfs/data/johnsonslab/nlp-genomics/t2d/T2D1.as2.NLM031/humann_raw_out/SRR341706_1_humann_temp/SRR341706_1_metaphlan_bowtie2.txt
