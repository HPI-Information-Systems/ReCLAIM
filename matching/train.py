import argparse
import json
import os
import random
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
from matching.utils.dataset import KunstgraphDataset

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="ditto")
    parser.add_argument("--run_id", type=str, default=0)
    parser.add_argument("--max_len", type=int, default=512)
    parser.add_argument("--n_epochs", type=int, default=20)
    parser.add_argument("--finetuning", dest="finetuning", action="store_true")
    parser.add_argument("--save_model", dest="save_model", action="store_true")
    parser.add_argument("--logdir", type=str, default="checkpoints/")
    parser.add_argument("--lm", type=str, default="distilbert")
    parser.add_argument("--da", type=str, default=None)
    parser.add_argument("--alpha_aug", type=float, default=0.8)
    parser.add_argument("--summarize", dest="summarize", action="store_true")
    parser.add_argument("--size", type=int, default=None)
    parser.add_argument("--seed_id", type=int, default=42)
    parser.add_argument("--find_lr", dest="find_lr", action="store_true")
    parser.add_argument("--freeze_bert", dest="freeze_bert", action="store_true")
    parser.add_argument("--batch_size", type=int, default=32)
    parser.add_argument("--dropout", type=float, default=0.0)
    parser.add_argument("--early_stop", dest="early_stop", action="store_true")
    parser.add_argument("--lr", type=float, default=3e-5)
    parser.add_argument("--adamw", dest="adamw", action="store_true")
    parser.add_argument(
        "--non_linear_ditto", dest="non_linear_ditto", action="store_true"
    )
    parser.add_argument("--clip_grad", dest="clip_grad", action="store_true")

    hp = parser.parse_args()

    batch_size = hp.batch_size

    # set seeds
    seed = Settings.random_seeds()[hp.seed_id]
    seed_everything(seed, workers=True)

    # create the tag of the run
    run_tag = "%s_lm=%s_size=%s_seed=%d_slurmId=%s" % (
        hp.model,
        Settings.lm_to_hugginface_name_map(hp.lm),
        str(hp.size),
        seed,
        str(hp.run_id),
    )

    run_tag = run_tag.replace("/", "_")

    GENERATOR = torch.Generator().manual_seed(seed)

    settings = Settings()

    data = pd.read_csv("data/labelled_data_dropped.csv", low_memory=False)

    data = data.sample(frac=1).reset_index(drop=True)
    wandb_logger = WandbLogger(
        project=settings.wandb_project,
        name=run_tag,
        entity=settings.wandb_entity,
        save_dir="/scratch/bp-naumann23/train",
        config={
            "batch_size": hp.batch_size,
            "epochs": hp.n_epochs,
            "lm": hp.lm,
            "max_len": hp.max_len,
            "seed": hp.seed_id,
            "drop": hp.dropout,
            "freeze_bert": hp.freeze_bert,
            "adamw": hp.adamw,
            "non_linear_ditto": hp.non_linear_ditto,
            "clip_grad": hp.clip_grad,
        },
    )

    data = DittoDataset(data, lm=hp.lm, max_len=hp.max_len, size=hp.size, da=hp.da)

    trainset, validset, testset = random_split(
        data, [0.64, 0.16, 0.2], generator=GENERATOR
    )

    num_steps = (len(trainset) // batch_size) * hp.n_epochs

    model = LitDittoModel(
        hp.lm,
        hp.alpha_aug,
        num_steps=num_steps,
        lr=hp.lr,
        run_id=run_tag,
        freeze_bert=hp.freeze_bert,
        drop=hp.dropout,
    )

    steps_per_batch = len(trainset) // batch_size

    torch.set_float32_matmul_precision("medium")

    trainer = L.Trainer(
        logger=wandb_logger,
        max_epochs=hp.n_epochs,
        default_root_dir="/scratch/bp-naumann23/train",
        num_sanity_val_steps=3,
        strategy="ddp_find_unused_parameters_true",
        gradient_clip_val=1.0 if hp.clip_grad else None,
    )

    padder = KunstgraphDataset.pad

    train_iter = DataLoader(
        dataset=trainset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=2,
        collate_fn=padder,
    )
    valid_iter = DataLoader(
        dataset=validset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=2,
        collate_fn=padder,
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
    lr_finder = tuner.lr_find(model, train_dataloaders=valid_iter)
    print(lr_finder.results)
    new_lr = lr_finder.suggestion()
    model.lr = new_lr

    if hp.model != "notrain":

        trainer.fit(
            model=model,
            train_dataloaders=train_iter,
            val_dataloaders=valid_iter,
        )

    if hp.model == "notrain":
        trainer.validate(
            model,
            dataloaders=valid_iter,
        )

    trainer.test(
        model,
        dataloaders=test_iter,
    )
