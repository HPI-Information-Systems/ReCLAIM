"""Adapted from https://github.com/megagonlabs/sudowoodo/blob/main/selfsl/augment.py"""

import json
import random

import numpy as np


class Augmenter(object):
    """Data augmentation operator.

    Support both span and attribute level augmentation operators.
    """

    def __init__(self):
        pass

    def augment(self, tokens, labels, op="del"):
        """Performs data augmentation on a sequence of tokens

        The supported ops:

        Args:
            tokens (list of strings): the input tokens
            labels (list of strings): the labels of the tokens
            op (str, optional): a string encoding of the operator to be applied

        Returns:
            list of strings: the augmented tokens
            list of strings: the augmented labels
        """
        if "drop_token" in op:
            new_tokens, new_labels = [], []
            for token, label in zip(tokens, labels):
                if label != "O" or random.randint(0, 4) != 0:
                    new_tokens.append(token)
                    new_labels.append(label)
            return new_tokens, new_labels
        elif "drop_col" in op:
            col_starts = [i for i in range(len(tokens)) if tokens[i] == "[COL]"]
            col_ends = [0] * len(col_starts)
            col_lens = [0] * len(col_starts)
            for i, pos in enumerate(col_starts):
                if i == len(col_starts) - 1:
                    col_lens[i] = len(tokens) - pos
                    col_ends[i] = len(tokens) - 1
                else:
                    col_lens[i] = col_starts[i + 1] - pos
                    col_ends[i] = col_starts[i + 1] - 1

                if tokens[col_ends[i]] == "[SEP]":
                    col_ends[i] -= 1
                    col_lens[i] -= 1
            candidates = [i for i, le in enumerate(col_lens) if le <= 8]
            if len(candidates) > 0:
                idx = random.choice(candidates)
                start, end = col_starts[idx], col_ends[idx]
                new_tokens = tokens[:start] + tokens[end + 1 :]
                new_labels = labels[:start] + labels[end + 1 :]
            else:
                new_tokens, new_labels = tokens, labels
        else:
            # raise ValueError('DA operator not found')
            new_tokens, new_labels = tokens, labels

        return new_tokens, new_labels

    def augment_sent(self, text, op="all"):
        """Performs data augmentation on a classification example.

        Similar to augment(tokens, labels) but works for sentences
        or sentence-pairs.

        Args:
            text (str): the input sentence
            op (str, optional): a string encoding of the operator to be applied

        Returns:
            str: the augmented sentence
        """
        # 50% of chance of flipping
        if " [SEP] " in text and random.randint(0, 1) == 0:
            left, right = text.split(" [SEP] ")
            text = right + " [SEP] " + left

        # tokenize the sentence
        current = ""
        tokens = text.split(" ")

        # avoid the special tokens
        labels = []
        for token in tokens:
            if token in ["[COL]", "[VAL]"]:
                labels.append("HD")
            elif token in ["[CLS]", "[SEP]"]:
                labels.append("<SEP>")
            else:
                labels.append("O")

        if op == "all":
            N = 5
            ops = ["drop_col", "drop_token"]
            for op in random.choices(ops, k=N):
                tokens, labels = self.augment(tokens, labels, op=op)

        results = " ".join(tokens)
        return results
