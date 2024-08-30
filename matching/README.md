# Matching

## Dependencies

To train the models, please install all required dependencies in a conda environment:

```bash
conda create --name matching --file=environment.yml
conda activate matching
```

The training was performed on a high performance computing cluster.
To train the model efficiently, please ensure that CUDA is installed and available on your system.

You can train the model on a CPU, but it will take significantly longer.

Please also update the `.env.example` file environment configuration and rename it to `.env`.

## Data

The data used for training the model is not included in this repository due to file size restrictions.
You can create a database dump by running the data loading cells of the `generate.ipynb` notebook.

The data should be located in the `./data/` directory.

## Training and Logging

To train the model, either run the `train.py` script using

```bash
python3 -u train.py
```

or schedule a job on the cluster.
To schedule a job on the cluster, connect to it, activate the conda environment and run

```bash
sbatch train.slurm
```

Training the model using `train.py` does not use pretraining.

To use pretraining, please use the `pretrain.py` file or schedule a job on the cluster using `pretrain.slurm`.

Both scripts spawn five different runs using different seeds.
Please refer to the respective help messages of the scripts to see all available arguments.
You can display the help message by running

```bash
python3 train.py --help
python3 pretrain.py --help
```

We use [wandb](https://wandb.ai/) to log the run values and later evaluate them.
Please create an account and log in to wandb using

```bash
    wandb login
```

Please change the wandb project names and entity in `matching/config.py` to match your project names.