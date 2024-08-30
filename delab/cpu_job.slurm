#!/bin/sh
#SBATCH -A naumann-bp2023fn1
#SBATCH --job-name=kunstgraph-myjob
#SBATCH --output=logs/output.log
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=8G
#SBATCH --gpus=0
#SBATCH --time=1:0:0
#SBATCH --constraint=ARCH:X86

poetry install

poetry run python -u my_script.py
