# Usage of the DE-Lab Cluster and SLURM

## Prerequistites

To make usage of the cluster easier, we will utilise local SSH keys - this way, you don't have to enter your HPI-password every time you want to connect to the cluster.

**You can only connect to the cluster while you are within the HPI network**

### Generate SSH keys

To generate a new SSH key, open a terminal and run the following command:

```bash
ssh-keygen -t ed25519
```

You will be asked to enter a file to save the key in. The default is `~/.ssh/id_ed25519`, which is fine. You can also enter a passphrase, but this is optional.

### Copy the SSH key to the cluster

To copy the SSH key to the cluster, run the following command:

```bash
ssh-copy-id -i <path-to-key>.pub <firstName>.<lastName>@delab.i.hpi.de
```

> **Important**: Upload _only_ the public key (`<path-to-key>.pub`) to the cluster. The private key should never leave your local machine.

Now authenticate with your HPI password. Afterwards, you should be able to connect to the cluster without entering your password.

### Connect to the cluster

To connect to the cluster, run the following command:

```bash
ssh <firstName>.<lastName>@delab.i.hpi.de
```

## SLURM

SLURM is a job scheduler that allows you to run jobs on the cluster.

Whenever you connect to the cluster, you will initially be on `lx01` or `lx02` - the login nodes. You should not run any computationally intensive tasks on these nodes.

To run a job on the cluster, you have to submit a job script to the SLURM scheduler.

### Starting an interactive terminal session

To start an interactive terminal session, run the following command:

```bash
salloc -A naumann-bp2023fn1 --time=1:00:00
```

This will allocate resources for you for 1 hour. You can adjust the time limit as needed. The `--time` flag takes the format `days-hours:minutes:seconds`.

An interactive session is useful for debugging or testing your code. Not for running long computations. Use the job scheduler for that.

In general, if you are on nodes tx01, or tx02, you can run your experiments.

### Starting a training job

To start a training job, you have to create a job script. Depending on the resources you need, you can choose between different partitions. The most important partitions are:

- magic: For CPU jobs
- sorcery: For GPU jobs

Please feel free to adapt one of the scripts in this directory to your needs.

If you want to write the console to a file, you can use the following command:

```bash
python my_script.py > <output-file>.out
```

in the job script.

To actually submit the job, run the following command:

```bash
sbatch <job-script>.slurm
```

# How to get the Repo on the Cluster

Currently, we are using a deploy key to clone the repository on the cluster.

To generate a new deploy key, run the following command:

```bash
ssh-keygen -t ed25519 "your_email"
```

on the **cluster**. You will be asked to enter a file to save the key in. The default is `~/.ssh/id_ed25519`, which is fine. You can also enter a passphrase, but this is optional.

Now, in your browser, navigate to our repository on [GitHub](https://www.github.com), go to `Settings` -> `Deploy keys` -> `Add deploy key` and paste the public key (`~/.ssh/id_ed25519.pub`) into the key field. Don't forget to give the key a title.

Now you can clone the repository on the cluster with the following command:

```bash
git clone git@github.com:bp2023-fn1/kunstgraph.git
```

using an ssh connection.

Note: It might be worth it giving the deploy key write access to the repository, so you can push changes from the cluster. This can be done in the same menu as before. However, **only** do this if you are absolutely certain that you need to write to the repository from the cluster, as the ssh keys on the cluster might not be protected by a passphrase.
Pushing from the cluster could, for example, be useful to store logs and trained models in the repository.

## Installing Poetry on the Cluster

To install Poetry on the cluster, run the following command:

```bash
pip install poetry
```

## Remote connections to the cluster

Before connecting, please activate an interactive session in the cluster, as described above.

To connect to the cluster from VS Code, you can use the Remote - SSH extension. To do this, you have to install the extension first.

Then, press `Ctrl+Shift+P` and search for `Remote-SSH: Add new SSH-Host...`. Enter the following command:

```bash
ssh <firstName>.<lastName>@tx01.delab.i.hpi.de
```

or

```bash
ssh <firstName>.<lastName>@tx02.delab.i.hpi.de
```

respectively.
