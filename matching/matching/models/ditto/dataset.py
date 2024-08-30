import numpy as np
import pandas as pd
from torch.utils import data

from ...utils.dataset import KunstgraphDataset


class DittoDataset(KunstgraphDataset):
    """Kunstgraph dataset"""

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
