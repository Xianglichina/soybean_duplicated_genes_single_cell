#!/bin/bash
#SBATCH --job-name=r_script
#SBATCH --partition=iob_highmem
#SBATCH --ntasks=1
#SBATCH --mem=600g
#SBATCH --time=3:00:00
#SBATCH --output=r_script.%j.out    # Standard output log
#SBATCH --error=r_script.%j.err     # Standard error log
#SBATCH --mail-type=END,FAIL          # Mail events (NONE, BEGIN, END, FAIL, ALL)


module load R/4.3.1-foss-2022a   
Rscript get_coexp_network_no_filter.r  early_nodule_normalized.csv





