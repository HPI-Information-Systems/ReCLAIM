#!/bin/sh
#SBATCH -A naumann-bp2023fn1
#SBATCH --job-name=kunstgraph-mygpujob
#SBATCH --output=logs/output.log
#SBATCH --partition sorcery
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=8G
#SBATCH --gpus=1

poetry install

poetry run python -u my_script.py
