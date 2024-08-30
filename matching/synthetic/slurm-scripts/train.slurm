#!/bin/sh
#SBATCH -A naumann-bp2023fn1
#SBATCH --job-name=kunstgraph-train
#SBATCH --output=logs/%j_output.log
#SBATCH --partition sorcery
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --gpus=1
#SBATCH --time 4:0:0
#SBATCH --constraint ARCH:X86

echo "Starting training for $1 with $2 epochs"

cd ~/ditto

CUDA_VISIBLE_DEVICES=0 ~/miniconda3/bin/python3 train_ditto.py --task $1 --batch_size 64 --max_len 64 --lr 3e-5 --n_epochs $2 --lm distilbert --fp16 --da del --summarize # --save_model
# Syntax: train.slurm <ditto_task> <n_epochs>
