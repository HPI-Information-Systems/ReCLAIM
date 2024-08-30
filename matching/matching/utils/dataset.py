"""
Adapted from https://github.com/megagonlabs/ditto.git
"""

import numpy as np
import pandas as pd
import torch
from torch.utils import data
from transformers import AutoTokenizer

from matching.config import Settings


def get_tokenizer(lm):
    return AutoTokenizer.from_pretrained(Settings.lm_to_hugginface_name_map(lm))


class KunstgraphDataset(data.Dataset):
    """EM dataset"""

    def __init__(
        self,
        df: pd.DataFrame,
        max_len=256,
        size=None,
        lm="roberta",
        da=None,
        set_labels=True,
    ):
        self.tokenizer = get_tokenizer(lm)
        self.pairs = []
        self.labels = []
        self.max_len = max_len
        self.size = size

        cols_1 = [col for col in df.columns if col.startswith("1_")]
        cols_2 = [col for col in df.columns if col.startswith("2_")]

        for col in cols_1 + cols_2:
            df[col] = df[col].astype(str)

        for _idx, line in df.iterrows():
            left = "[COL] "
            for col in cols_1:
                if col == "1_uri":
                    continue
                if line[col] != "nan":
                    left += (
                        str(col).replace("1_", "")
                        + " [VAL] "
                        + str(line[col]).replace("1_", "")
                        + " [COL] "
                    )

            right = "[COL] "
            for col in cols_2:
                if col == "2_uri":
                    continue
                # check if the value is not nan
                if (val := line[col]) != "nan" and val is not None:
                    right += (
                        str(col).replace("2_", "")
                        + " [VAL] "
                        + str(line[col]).replace("2_", "")
                        + " [COL] "
                    )

            # remove the last COL
            right = right[:-6]
            left = left[:-6]

            if set_labels:
                label = line["label"]
                self.labels.append(int(label))
            else:
                self.labels.append(1)

            self.pairs.append((left, right))

        self.pairs = self.pairs[:size]

        if set_labels:
            self.labels = self.labels[:size]

        self.da = da

    def __len__(self):
        """Return the size of the dataset."""
        return len(self.pairs)

    def __getitem__(self, idx):
        """Return a tokenized item of the dataset.

        Args:
            idx (int): the index of the item

        Returns:
            List of int: token ID's of the two entities
            List of int: token ID's of the two entities augmented (if da is set)
            int: the label of the pair (0: unmatch, 1: match)
        """
        left = self.pairs[idx][0]
        right = self.pairs[idx][1]

        x = self.tokenizer.encode(
            text=left, text_pair=right, truncation=True, max_length=self.max_len
        )

        return np.array(x), self.labels[idx]

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

        if len(batch[0]) == 3:
            x1, x2, y = zip(*batch)

            maxlen = max([len(x) for x in x1 + x2])
            x1 = [np.append(xi, [0] * (maxlen - len(xi))) for xi in x1]
            x2 = [np.append(xi, [0] * (maxlen - len(xi))) for xi in x2]
            return (
                torch.LongTensor(np.array(x1)),
                torch.LongTensor(np.array(x2)),
                torch.LongTensor(np.array(y)),
            )
        else:
            if isinstance(batch[0][1], int):
                x12, y = zip(*batch)
                maxlen = max([len(x) for x in x12])

                x12 = [np.append(xi, [0] * (maxlen - len(xi))) for xi in x12]
                return torch.LongTensor(np.array(x12)), torch.LongTensor(np.array(y))

            x1, x2 = zip(*batch)

            maxlen = max([len(x) for x in x1 + x2])
            x1 = [np.append(xi, [0] * (maxlen - len(xi))) for xi in x1]
            x2 = [np.append(xi, [0] * (maxlen - len(xi))) for xi in x2]
            return (
                torch.LongTensor(np.array(x1)),
                torch.LongTensor(np.array(x2)),
            )
