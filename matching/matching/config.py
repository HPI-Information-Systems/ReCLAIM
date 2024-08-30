"""
Contains configuration for the matching algorithms. You can specify the multiplier for the loss for false-positives here, for example
"""

from typing import List


class Settings:
    def __init__(self):
        self.drop_foreign_keys = True

        self.model_name = "ditto"

        self.wandb_project = "Matching"
        self.wandb_pretrain_project = "Matching-Pretrain"
        self.wandb_entity = "bp2023fn1-kunstgraph"

    @staticmethod
    def get_serialisation_format():
        return "ditto"

    @staticmethod
    def lm_to_hugginface_name_map(lm: str) -> str:
        lm_mp = {
            "roberta": "roberta-base",
            "distilbert": "distilbert-base-uncased",
        }

        if lm in lm_mp:
            return lm_mp[lm]
        else:
            return lm

    @staticmethod
    def random_seeds() -> List[int]:
        return [0, 4555, 6218, 5548, 42]


def get_settings() -> Settings:
    return Settings()
