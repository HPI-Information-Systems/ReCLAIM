"""
Adapted from https://github.com/megagonlabs/sudowoodo/blob/main/selfsl/bt_dataset.py
"""

import random
import numpy as np
import pandas as pd
import torch
from torch.utils import data
from transformers import AutoTokenizer
from .augment import Augmenter

from matching.config import Settings
from matching.utils.serialise import serialise_entity


def get_tokenizer(lm):
    return AutoTokenizer.from_pretrained(Settings.lm_to_hugginface_name_map(lm))


class PretrainDataset(data.Dataset):
    """Pretrain dataset"""

    def __init__(
        self,
        df: pd.DataFrame,
        max_len=256,
        size=None,
        lm="roberta",
        da="all",
    ):
        self.tokenizer = get_tokenizer(lm)
        self.data = []

        self.max_len = max_len
        self.size = size

        for _idx, line in df.iterrows():
            left = serialise_entity(line, exclude_uri=True)
            self.data.append(left)

        if size is not None:
            if size > len(self.data):
                N = size // len(self.data) + 1
                self.data = (self.data * N)[:size]
            else:
                self.data = random.sample(self.data, size)

        self.augmenter = Augmenter()

        self.da = da


    def __len__(self):
        """Return the size of the dataset."""
        return len(self.data)

    def __getitem__(self, idx):
        """Return a tokenized item of the dataset.

        Args:
            idx (int): the index of the item

        Returns:
            List of int: token ID's of the 1st entity
            List of int: token ID's of the 2nd entity
            List of int: token ID's of the two entities combined
            int: the label of the pair (0: unmatch, 1: match)
        """
        A = self.data[idx]
        B = self.augmenter.augment_sent(A, self.da)

        # left
        yA = self.tokenizer.encode(text=A,
                                   max_length=self.max_len,
                                   truncation=True)
        yB = self.tokenizer.encode(text=B,
                                   max_length=self.max_len,
                                   truncation=True)
        return yA, yB


    @staticmethod
    def pad(batch):
        """Merge a list of dataset items into a train/test batch
        Args:
            batch (list of tuple): a list of dataset items

        Returns:
            Float: x1 of shape (batch_size, seq_len)
            Float: x2 of shape (batch_size, seq_len).
                        Elements of x1 and x2 are padded to the same length
            Float: a batch of labels, (batch_size,)
        """

        yA, yB = zip(*batch)

        max_len = max([len(x) for x in yA])
        max_len = max(max_len,max([len(x) for x in yB]))

        yA = [xi + [0]*(max_len - len(xi)) for xi in yA]
        yB = [xi + [0]*(max_len - len(xi)) for xi in yB]

        return torch.LongTensor(yA), torch.LongTensor(yB)

