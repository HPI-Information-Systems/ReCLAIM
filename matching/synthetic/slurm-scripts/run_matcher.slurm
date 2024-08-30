#!/bin/sh
#SBATCH -A naumann-bp2023fn1
#SBATCH --job-name=kunstgraph-matcher
#SBATCH --output=logs/output.log
#SBATCH --partition sorcery
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --gpus=1
#SBATCH --time 1:0:0
#SBATCH --constraint ARCH:X86

cd ~/ditto

CUDA_VISIBLE_DEVICES=0 ~/miniconda3/bin/python3 matcher.py --task $2 --input_path input/$1 --output_path output/$2_results_$1 --lm distilbert --max_len 64 --use_gpu --fp16 --summarize --checkpoint_path checkpoints/
# Syntax: run_matcher.slurm <candidates_jsonl_file> <ditto_task>
# Candidates file must be in ditto/input directory.
