#!/bin/sh
#SBATCH -A naumann-bp2023fn1
#SBATCH --job-name=kunstgraph-train
#SBATCH --output=logs/output_%A_%a.log
#SBATCH --nodes 1
#SBATCH --partition sorcery
#SBATCH --cpus-per-task 6
#SBATCH --mem 128G
#SBATCH --gpus 1
#SBATCH --time 2-0:0:0
#SBATCH -C "GPU_MEM:40GB&ARCH:X86"
#SBATCH --array=0-4

srun python3 -u train.py --n_epochs 10 --lm distilbert --seed_id $SLURM_ARRAY_TASK_ID  --run_id $SLURM_ARRAY_JOB_ID --find_lr\
    --batch_size=32
