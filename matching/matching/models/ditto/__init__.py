import os
import time

import lightning as L
import numpy as np
import pandas as pd
import torch
from torch import nn
from torchmetrics.classification import BinaryF1Score, BinaryPrecision, BinaryRecall
from transformers import AutoModel, get_linear_schedule_with_warmup

from matching.config import get_settings
from matching.models.pretrained import PretrainedBERT


class LitDittoModel(L.LightningModule):
    def __init__(
        self,
        lm="roberta",
        alpha_aug=0.8,
        use_pretrained=False,
        pretrained_model: PretrainedBERT = None,
        lr=3e-5,
        weights=torch.tensor([1.0, 4.0]),
        num_steps=1000,
        run_id=None,
        freeze_bert=False,
        seed_nr=0,
        drop=0.0,
    ):
        super().__init__()

        self.alpha_aug = alpha_aug

        self.run_id = time.strftime("%d-%m-%H-%M-%S")

        # Model
        if use_pretrained:
            self.bert = pretrained_model.bert
        else:
            self.bert = AutoModel.from_pretrained(
                get_settings().lm_to_hugginface_name_map(lm)
            )

        # linear layer
        hidden_size = self.bert.config.hidden_size
        self.fc = torch.nn.Linear(hidden_size, 2)

        self.freeze_bert = freeze_bert
        self.num_steps = num_steps

        self.criterion = nn.CrossEntropyLoss(weight=weights)

        self.f1 = BinaryF1Score(threshold=0.5)  # Default threshold for initialization

        self.dropout = nn.Dropout(p=drop)

        self.best_f1_score = 0.0
        self.best_threshold = 0.5
        self.thresholds = [
            i / 20.0 for i in range(1, 20)
        ]  # Thresholds from 0.05 to 0.95

        self.precision = BinaryPrecision()
        self.recall = BinaryRecall()

        self.run_id = run_id
        self.seed_nr = seed_nr

        self.lr = lr

    def forward(self, x1: torch.tensor, x2=None):
        """Encode the left, right, and the concatenation of left+right.

        Args:
            x1 (LongTensor): a batch of ID's
            x2 (LongTensor, optional): a batch of ID's (augmented)

        Returns:
            Tensor: binary prediction
        """

        attention_mask = []

        for sentence in x1:
            sentence_mask = []
            for elem in sentence:
                if elem == 0:
                    sentence_mask.append(0)
                else:
                    sentence_mask.append(1)

            attention_mask.append(sentence_mask)

        attention_mask = torch.tensor(attention_mask).to(x1.device)

        if x2 is not None:
            # MixDA
            if self.freeze_bert:
                with torch.no_grad():
                    enc = self.bert(torch.cat((x1, x2)))[0][:, 0, :]
            else:
                enc = self.bert(torch.cat((x1, x2)))[0][:, 0, :]
            batch_size = len(x1)
            enc1 = enc[:batch_size]  # (batch_size, emb_size)
            enc2 = enc[batch_size:]  # (batch_size, emb_size)

            aug_lam = np.random.beta(self.alpha_aug, self.alpha_aug)
            enc = enc1 * aug_lam + enc2 * (1.0 - aug_lam)
        else:
            if self.freeze_bert:
                with torch.no_grad():
                    enc = self.bert(x1, attention_mask=attention_mask)[0][:, 0, :]
            else:
                enc = self.bert(x1, attention_mask=attention_mask)[0][:, 0, :]

        return self.fc(self.dropout(enc))

    def training_step(self, batch, batch_idx):
        if len(batch) == 3:
            x1, x2, y = batch
            prediction = self.forward(x1, x2)
        else:
            x, y = batch
            prediction = self.forward(x)

        loss = self.criterion(prediction, y)

        self.log("train_loss", loss, sync_dist=True)

        return loss

    def test_step(self, batch, batch_idx):
        if len(batch) == 3:
            x1, x2, y = batch
            prediction = self.forward(x1, x2)
        else:
            x, y = batch
            prediction = self.forward(x)
        loss = self.criterion(prediction, y)
        self.log("test_loss", loss, sync_dist=True)

        probs = prediction.softmax(dim=1)[:, 1]

        self.f1.threshold = self.best_threshold
        self.log("test_f1", self.f1(probs, y), sync_dist=True)
        self.f1.reset()

        self.precision.threshold = self.best_threshold
        self.precision.update(probs, y)
        self.log("test_precision", self.precision.compute(), sync_dist=True)
        self.precision.reset()

        self.recall.threshold = self.best_threshold
        self.recall.update(probs, y)
        self.log("test_recall", self.recall.compute(), sync_dist=True)
        self.recall.reset()

        os.makedirs("./data/output", exist_ok=True)

        predictions_output = torch.cat(
            [y.unsqueeze(1), prediction.softmax(dim=1)], dim=1
        )

        output_path = "./data/output/predictions.csv"
        df = predictions_output.cpu().detach().numpy()
        df = pd.DataFrame(
            df, columns=["label", "probability_no_match", "probability_match"]
        )

        df["run_id"] = self.run_id or "default"
        df["batch_idx"] = batch_idx
        df["best_threshold"] = self.best_threshold

        df.to_csv(output_path, mode="a", header=not os.path.exists(output_path))

    def validation_step(self, batch, batch_idx):
        if len(batch) == 3:
            x1, x2, y = batch
            prediction = self.forward(x1, x2)
        else:
            x, y = batch
            prediction = self.forward(x)

        loss = self.criterion(prediction, y)
        self.log("val_loss", loss, sync_dist=True)

        probs = prediction.softmax(dim=1)[:, 1]

        best_f1 = 0.0
        best_threshold = 0.5

        for threshold in self.thresholds:
            self.f1.threshold = threshold
            f1_score = self.f1(probs, y)
            self.log(f"val_f1_{threshold}", f1_score, sync_dist=True)
            self.f1.reset()

            if f1_score > best_f1:
                best_f1 = f1_score
                best_threshold = threshold

        if best_f1 > self.best_f1_score:
            self.best_f1_score = best_f1
            self.best_threshold = best_threshold

        self.f1.threshold = self.best_threshold
        self.log("best_val_f1", self.f1(probs, y), sync_dist=True)
        self.f1.reset()
        self.log("best_threshold", self.best_threshold)

    def configure_optimizers(self):
        optimizer = torch.optim.AdamW(self.parameters(), lr=self.lr)

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
