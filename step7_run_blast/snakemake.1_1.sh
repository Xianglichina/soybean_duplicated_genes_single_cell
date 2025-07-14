#!/bin/bash
#SBATCH --job-name=snakemake
#SBATCH --partition=iob_highmem
#SBATCH --ntasks=1
#SBATCH --mem=600g
#SBATCH --time=144:00:00
#SBATCH --output=snakemake.%j.out    # Standard output log
#SBATCH --error=snakemake.%j.err     # Standard error log
#SBATCH --mail-type=END,FAIL          # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=xl20359@uga.edu  # Where to send mail (change username@uga.edu to your email address

export PATH=/home/xl20359/condaenv_v2/bin:$PATH
source activate /home/xl20359/condaenv_v2/envs/snakemake_v1
snakemake -prs 0117_snakemake.1_1  --profile /home/xl20359/.config/snakemake/batchsub/ --unlock
snakemake -prs 0117_snakemake.1_1  --profile /home/xl20359/.config/snakemake/batchsub/
