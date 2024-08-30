from math import exp
import sys
import lightning as L
from matching.config import Settings
import torch
import torch.nn as nn
from torch import cosine_embedding_loss
import torch.nn.functional as F
import numpy as np

from transformers import AutoModel, get_linear_schedule_with_warmup


class PretrainedBERT(L.LightningModule):
    def __init__(
        self,
        lm="roberta",
        lr=3e-6,
        max_len=256,
        num_steps=1000,
        temperature=0.07,
        batch_size=32,
        non_linear=False,
        dropout=0.6,
        **kwargs,
    ):
        super().__init__()

        self.bert = AutoModel.from_pretrained(Settings.lm_to_hugginface_name_map(lm))

        hidden_size = self.bert.config.hidden_size

        self.temperature = temperature
        self.batch_size = batch_size
        self.n_views = 2
        self.lr = lr
        self.max_len = max_len
        self.num_steps = num_steps

        self.projector = nn.Linear(hidden_size, hidden_size)
        self.dropout = nn.Dropout(dropout)
        self.relu = nn.ReLU()

        # normalization layer for the representations z1 and z2

        self.non_linear = non_linear
        self.bn = nn.BatchNorm1d(hidden_size, affine=False)

        self.criterion = nn.CrossEntropyLoss()

    def info_nce_loss(self, features, batch_size):
        """Copied from https://github.com/sthalles/SimCLR/blob/master/simclr.py"""
        labels = torch.cat(
            [torch.arange(batch_size) for i in range(self.n_views)], dim=0
        )
        labels = (labels.unsqueeze(0) == labels.unsqueeze(1)).float()
        labels = labels.to(self.device)

        features = F.normalize(features, dim=1).to(self.device)

        similarity_matrix = torch.matmul(features, features.T)

        mask = torch.eye(labels.shape[0], dtype=torch.bool)
        labels = labels[~mask].view(labels.shape[0], -1)

        similarity_matrix = similarity_matrix[~mask].view(
            similarity_matrix.shape[0], -1
        )

        positives = similarity_matrix[labels.bool()].view(labels.shape[0], -1)

        negatives = similarity_matrix[~labels.bool()].view(
            similarity_matrix.shape[0], -1
        )

        logits = torch.cat([positives, negatives], dim=1)
        labels = torch.zeros(logits.shape[0], dtype=torch.long).to(self.device)

        logits = logits / self.temperature
        return logits, labels

    def forward(self, x1, x2):
        attention_mask = []

        y = torch.cat((x1, x2))

        for sentence in y:
            sentence_mask = []
            for elem in sentence:
                if elem == 0:
                    sentence_mask.append(0)
                else:
                    sentence_mask.append(1)

            attention_mask.append(sentence_mask)

        attention_mask = torch.tensor(attention_mask).to(y.device)

        if self.non_linear:
            return self.projector(
                self.dropout(
                    self.relu(self.bert(y, attention_mask=attention_mask)[0][:, 0, :])
                )
            )
        else:
            return self.projector(
                self.dropout(self.bert(y, attention_mask=attention_mask)[0][:, 0, :])
            )

    def training_step(self, batch, batch_idx):
        x1, x2 = batch

        z = self.forward(x1, x2)

        batch_size = len(x1)

        logits, labels = self.info_nce_loss(z, batch_size)
        loss = self.criterion(logits, labels)

        self.log("pretrain_loss", loss)

        return loss

    def validation_step(self, batch, batch_idx):
        x1, x2 = batch

        z = self.forward(x1, x2)
        batch_size = len(x1)

        logits, labels = self.info_nce_loss(z, batch_size)
        loss = self.criterion(logits, labels)

        self.log("pretrain_val_loss", loss)

        return loss

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=self.lr)

        scheduler = get_linear_schedule_with_warmup(
            optimizer,
            num_warmup_steps=0,
            num_training_steps=self.num_steps,
        )

        return {
            "optimizer": optimizer,
            "lr_scheduler": {
                "scheduler": scheduler,
                "interval": "step",  # Update the scheduler at each step
                "frequency": 1,
            },
        }
