#!/bin/bash
#SBATCH -J braindata
#SBATCH --time=0-1:00:00
#SBATCH -n 16
#SBATCH --mem=64000
#SBATCH --array=1-7

module load R/4.2.2
cd /cluster/tufts/hcilab/mrusse06/hcijs/ml

Rscript --vanilla _brms.r $SLURM_ARRAY_TASK_ID

