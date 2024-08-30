"""
Contains the data generation and code used for contrastive pre-training of the SBERT model.
"""

import argparse
import os

from dotenv import load_dotenv

load_dotenv()
import sys

import lightning as L
import numpy as np
import pandas as pd
import torch
from lightning.pytorch import seed_everything
from lightning.pytorch.loggers import WandbLogger
from lightning.pytorch.tuner import Tuner
from torch.utils.data import DataLoader, random_split

from matching.config import Settings
from matching.models.ditto import LitDittoModel
from matching.models.ditto.dataset import DittoDataset
from matching.models.pretrained import PretrainedBERT
from matching.models.pretrained.dataset import PretrainDataset
from matching.pretrain.generate import PretrainPairGenerator

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--run_id", type=str, default=0)
    parser.add_argument("--max_len", type=int, default=512)
    parser.add_argument("--n_pretrain_epochs", type=int, default=10)
    parser.add_argument("--n_epochs", type=int, default=10)
    parser.add_argument("--finetuning", dest="finetuning", action="store_true")
    parser.add_argument("--save_model", dest="save_model", action="store_true")
    parser.add_argument("--logdir", type=str, default="checkpoints/")
    parser.add_argument("--lm", type=str, default="distilbert")
    parser.add_argument("--fp16", dest="fp16", action="store_true")
    parser.add_argument("--da", type=str, default=None)
    parser.add_argument("--alpha_aug", type=float, default=0.8)
    parser.add_argument("--dk", type=str, default=None)
    parser.add_argument("--seed_id", type=int, default=42)
    parser.add_argument("--train", dest="train", action="store_true", default=False)
    parser.add_argument("--size", type=int, default=None)
    parser.add_argument("--generate_data", dest="generate_data", action="store_true")
    parser.add_argument("--find_lr", dest="find_lr", action="store_true")
    parser.add_argument("--batch_size", type=int, default=32)
    parser.add_argument("--comment", type=str, default="")
    parser.add_argument("--non_linear", dest="non_linear", action="store_true")
    parser.add_argument("--dropout", type=float, default=0.0)
    parser.add_argument("--freeze_bert", dest="freeze_bert", action="store_true")
    parser.add_argument("--early_stop", dest="early_stop", action="store_true")
    parser.add_argument("--lr", type=float, default=3e-5)
    parser.add_argument("--pretrain_dropout", type=float, default=0.6)
    parser.add_argument("--adamw", dest="adamw", action="store_true")
    parser.add_argument(
        "--non_linear_ditto", dest="non_linear_ditto", action="store_true"
    )
    parser.add_argument("--batch_overfit", dest="batch_overfit", action="store_true")
    parser.add_argument("--clip_grad", dest="clip_grad", action="store_true")

    hp = parser.parse_args()

    batch_size = hp.batch_size

    settings = Settings()

    seed = Settings.random_seeds()[hp.seed_id]
    seed_everything(seed, workers=True)

    run_tag = "pretrain_lm=%s_size=%s_seed=%d_slurmId=%s" % (
        Settings.lm_to_hugginface_name_map(hp.lm),
        str(hp.size),
        seed,
        str(hp.run_id),
    )

    run_tag = run_tag.replace("/", "_")

    generator = torch.Generator().manual_seed(seed)
    torch.set_float32_matmul_precision("medium")

    wandb_logger = WandbLogger(
        project=settings.wandb_pretrain_project,
        name=run_tag,
        entity=settings.wandb_entity,
        save_dir="/scratch/bp-naumann23/pretrain",
        config={
            "comment": hp.comment,
            "batch_size": hp.batch_size,
            "lm": hp.lm,
            "epochs": hp.n_epochs,
            "pretrain_epochs": hp.n_pretrain_epochs,
            "linear": hp.non_linear,
            "dropout": hp.dropout,
            "freeze_bert": hp.freeze_bert,
            "pretrain_dropout": hp.pretrain_dropout,
            "non_linear_ditto": hp.non_linear_ditto,
            "batch_overfit": hp.batch_overfit,
            "clip_grad": hp.clip_grad,
        },
    )

    instances = pd.read_csv("data/database_dump.csv")
    labelled_data = pd.read_csv("data/labelled_data_dropped.csv")

    instances = PretrainPairGenerator.generate_data_subset(
        instances, labelled_samples=labelled_data
    )
    pretrain_dataset = PretrainDataset(
        df=instances,
        max_len=hp.max_len,
        lm=hp.lm,
    )

    train, val, test = random_split(
        pretrain_dataset, [0.9, 0.099, 0.001], generator=generator
    )

    num_steps = (len(train) // batch_size) * hp.n_epochs

    torch.set_float32_matmul_precision("medium")

    pretrainer = L.Trainer(
        logger=wandb_logger,
        profiler="simple",
        max_epochs=hp.n_pretrain_epochs,
        default_root_dir="/scratch/bp-naumann23/pretrain",
        num_sanity_val_steps=3,
        strategy="ddp_find_unused_parameters_true",
    )

    model = PretrainedBERT(
        lm=hp.lm,
        max_len=hp.max_len,
        num_steps=num_steps,
        non_linear=hp.non_linear,
        lr=5e-5,
        dropout=hp.pretrain_dropout,
    )

    padder = pretrain_dataset.pad

    pretrain_iter = DataLoader(
        dataset=train,
        shuffle=True,
        batch_size=batch_size,
        num_workers=2,
        collate_fn=padder,
        pin_memory=True,
    )

    pretrain_val_iter = DataLoader(
        dataset=val,
        batch_size=batch_size,
        shuffle=False,
        num_workers=2,
        collate_fn=padder,
    )

    if hp.find_lr:
        tuner = Tuner(pretrainer)

        lr_finder = tuner.lr_find(model, train_dataloaders=pretrain_iter)

        print(lr_finder.results)

        new_lr = lr_finder.suggestion()

        model.lr = new_lr

    pretrainer.fit(
        model, train_dataloaders=pretrain_iter, val_dataloaders=pretrain_val_iter
    )

    if not hp.train:
        sys.exit(0)

    data = pd.read_csv("data/labelled_data_dropped.csv", low_memory=False)

    data = data.sample(frac=1).reset_index(drop=True)

    data = DittoDataset(data, lm=hp.lm, max_len=hp.max_len, size=hp.size, da=hp.da)

    ditto = LitDittoModel(
        use_pretrained=True,
        pretrained_model=model,
        run_id=run_tag,
        seed_nr=hp.seed_id,
        drop=hp.dropout,
        freeze_bert=hp.freeze_bert,
        lr=hp.lr,
    )

    trainset, validset, testset = random_split(data, [0.64, 0.16, 0.2])

    steps_per_batch = len(trainset) // batch_size

    torch.set_float32_matmul_precision("medium")

    trainer = L.Trainer(
        logger=wandb_logger,
        profiler="simple",
        max_epochs=hp.n_epochs,
        default_root_dir="/scratch/bp-naumann23/",
        num_sanity_val_steps=3,
        strategy="ddp_find_unused_parameters_true",
        gradient_clip_val=1.0 if hp.clip_grad else None,
    )

    padder = trainset.dataset.pad

    train_iter = DataLoader(
        dataset=trainset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=2,
        collate_fn=padder,
        pin_memory=True,
    )
    valid_iter = DataLoader(
        dataset=validset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=2,
        collate_fn=padder,
        pin_memory=True,
    )
    test_iter = DataLoader(
        dataset=testset,
        batch_size=batch_size * 16,
        shuffle=False,
        num_workers=2,
        collate_fn=padder,
        pin_memory=True,
    )

    tuner = Tuner(trainer)
    lr_finder = tuner.lr_find(ditto, train_dataloaders=train_iter, num_training=250)
    print(lr_finder.results)
    new_lr = lr_finder.suggestion()
    ditto.lr = new_lr

    trainer.fit(
        model=ditto,
        train_dataloaders=train_iter,
        val_dataloaders=valid_iter,
    )

    trainer.test(
        ditto,
        dataloaders=test_iter,
    )
