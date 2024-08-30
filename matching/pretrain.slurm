#!/bin/sh
#SBATCH -A naumann-bp2023fn1
#SBATCH --job-name=kunstgraph-pretrain
#SBATCH --output=logs/output_pretrain_%A_%a.log
#SBATCH --nodes 1
#SBATCH --partition sorcery
#SBATCH --cpus-per-task 6
#SBATCH --mem 128G
#SBATCH --gpus 1
#SBATCH --time 3-12:0:0
#SBATCH -C "GPU_MEM:40GB&ARCH:X86"
#SBATCH --array=0-4

N_EPOCHS=10
LM=distilbert
BATCH_SIZE=32

srun python3 -u pretrain.py --n_pretrain_epochs 2 --n_epochs $N_EPOCHS --lm $LM --seed_id $SLURM_ARRAY_TASK_ID --train --run_id $SLURM_ARRAY_JOB_ID\
                --find_lr --non_linear --batch_size=$BATCH_SIZE --pretrain_dropout 0.6 --freeze_bert
