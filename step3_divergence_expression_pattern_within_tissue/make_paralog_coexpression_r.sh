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
Rscript get_paralog_coexpression.r expressed_early_nodule_pairs_expression_separated.csv  early_nodule_coexp_network.Rdata




