import json
import random
from columns import (
    DATASET_SIZE,
    titles_simple,
    titles_with_synonyms,
    titles_with_translation,
    titles_with_antonyms,
)
from columns.augmentation_methods import AugmentationMethods
from columns.title import get_random_equal_titles, get_random_nonequal_titles
from columns.creator import get_random_equal_persons, get_random_nonequal_persons
from columns.gpt.mutually_exclusive_man import *
from columns.gpt.mutually_exclusive_woman import *
from columns.gpt.mutually_exclusive_objects import *
from columns.gpt.similar_nonmatches import *

import multiprocessing
from itertools import product

synthetic_fields = ["Title", "Creator"]
oversampling_factor = 1.2
NUM_FLAGS = 9


def generate_negative_match_pair(
    fetch_titles_from: list, flags: AugmentationMethods
) -> list[dict]:
    synthetic_entity = dict()
    synthetic_entity_no_match = dict()

    # Minimum number of fields that must be different is one
    num_nonequal_fields = random.randint(1, len(synthetic_fields))
    nonequal_fields = random.sample(synthetic_fields, num_nonequal_fields)

    if "Title" in nonequal_fields:
        title_1, title_2 = get_random_nonequal_titles(fetch_titles_from, flags)
    else:
        title_1, title_2 = get_random_equal_titles(fetch_titles_from, flags)

    if "Creator" in nonequal_fields:
        person_1, person_2 = get_random_nonequal_persons(flags)
    else:
        person_1, person_2 = get_random_equal_persons(flags)

    synthetic_entity["Title"] = title_1
    synthetic_entity["Creator"] = person_1

    synthetic_entity_no_match["Title"] = title_2
    synthetic_entity_no_match["Creator"] = person_2

    return [synthetic_entity, synthetic_entity_no_match]


def generate_positive_match_pair(
    fetch_titles_from: list, flags: AugmentationMethods
) -> list[dict]:
    synthetic_entity = dict()
    synthetic_entity_match = dict()

    title_1, title_2 = get_random_equal_titles(fetch_titles_from, flags)
    person_1, person_2 = get_random_equal_persons(flags)

    synthetic_entity["Title"] = title_1
    synthetic_entity["Creator"] = person_1

    synthetic_entity_match["Title"] = title_2
    synthetic_entity_match["Creator"] = person_2

    return [synthetic_entity, synthetic_entity_match]


def get_gpt_nonmatch_pairs(flags: AugmentationMethods) -> list[list[dict]]:
    return_pairs = []

    for m in similar_nonmatches_de + similar_nonmatches_en + mutually_exclusive_objects:
        synthetic_entity = dict()
        synthetic_entity_no_match = dict()

        # Minimum number of fields that must be different is one
        num_nonequal_fields = random.randint(1, len(synthetic_fields))
        nonequal_fields = random.sample(synthetic_fields, num_nonequal_fields)

        if "Creator" in nonequal_fields:
            person_1, person_2 = get_random_nonequal_persons(flags)
        else:
            person_1, person_2 = get_random_equal_persons(flags)

        title_1, title_2 = random.sample(m, 2)
        synthetic_entity["Title"] = title_1
        synthetic_entity_no_match["Title"] = title_2

        synthetic_entity["Creator"] = person_1
        synthetic_entity_no_match["Creator"] = person_2

        return_pairs.append([synthetic_entity, synthetic_entity_no_match])

    return return_pairs


def write_training_data(training_data, exp_name):
    split = int(len(training_data) / 4)

    with open(f"synthetic_output/{exp_name}_train.txt", "w", encoding="utf-8") as f:
        for line in training_data[: split * 3]:
            f.write(line + "\n")

    with open(f"synthetic_output/{exp_name}_valid.txt", "w", encoding="utf-8") as f:
        for line in training_data[split * 3 :]:
            f.write(line + "\n")


def write_input_data(training_data):
    with open("synthetic_output/synthetic_input.jsonl", "w", encoding="utf-8") as f:
        for line in training_data:
            f.write(line + "\n")


def pair_to_ditto(pair: list[dict], is_match: str) -> str:
    """line = ""
    for field in synthetic_fields:
        line += f"{pair[0][field]},"
        line += f"{pair[1][field]},"
    line += f"{is_match}"
    return line"""
    return (
        " ".join(f"COL {field} VAL {pair[0][field]}" for field in synthetic_fields)
        + "\t"
        + " ".join(f"COL {field} VAL {pair[1][field]}" for field in synthetic_fields)
        + f"\t{is_match}"
    )


def main(
    flags: AugmentationMethods,
    exp_name: str = "",
):
    training_data = []

    synthset_size = DATASET_SIZE * oversampling_factor
    num_iterations = int(synthset_size / 3)

    fetch_titles_from = titles_simple

    if flags.use_translations:
        fetch_titles_from += titles_with_translation
    if flags.use_synonyms:
        fetch_titles_from += titles_with_synonyms
    if flags.use_antonyms:
        fetch_titles_from += titles_with_antonyms

    for i in range(num_iterations):
        training_data.append(
            pair_to_ditto(
                generate_positive_match_pair(
                    fetch_titles_from, flags
                ),  # samples 1 item
                "1",
            )
        )
        training_data.append(
            pair_to_ditto(
                generate_negative_match_pair(
                    fetch_titles_from, flags
                ),  # samples 2 items
                "0",
            )
        )

        if i % 10000 == 0 and i != 0:
            print(f"Generated {i}/{num_iterations} pairs")

    # training_data += [pair_to_ditto(pair, "0") for pair in get_gpt_nonmatch_pairs(flags)]

    random.shuffle(training_data)
    write_training_data(training_data, exp_name)

    # training_data = ["1_Title,2_Title,1_Creator,2_Creator,label"] + training_data
    """ with open('synthetic_data/all.txt', 'w', encoding='utf-8') as f:
        for line in training_data:
            f.write(line + "\n") """


if __name__ == "__main__":
    processes = []
    ditto_configurations = []

    with open("configs.json", "r", encoding="utf-8") as f:
        ditto_configurations = json.load(f)

    """
    AugmentationMethods(
            use_deletion=True,
            use_shuffle=True,
            use_append_random_significant_words=True,
            use_translations=True,
            use_typos=True,
            use_append_random_date=True,
            use_abbreviations=True,
            use_synonyms=True,
            use_antonyms=True,
        ),
    """
    experiments = []

    experiments.extend(
        [
            AugmentationMethods(
                use_deletion=True,
                use_shuffle=False,
                use_append_random_significant_words=False,
                use_translations=False,
                use_typos=False,
                use_append_random_date=False,
                use_abbreviations=False,
                use_synonyms=False,
                use_antonyms=False,
            ),
            AugmentationMethods(
                use_deletion=False,
                use_shuffle=True,
                use_append_random_significant_words=False,
                use_translations=False,
                use_typos=False,
                use_append_random_date=False,
                use_abbreviations=False,
                use_synonyms=False,
                use_antonyms=False,
            ),
            AugmentationMethods(
                use_deletion=False,
                use_shuffle=False,
                use_append_random_significant_words=True,
                use_translations=False,
                use_typos=False,
                use_append_random_date=False,
                use_abbreviations=False,
                use_synonyms=False,
                use_antonyms=False,
            ),
            AugmentationMethods(
                use_deletion=False,
                use_shuffle=False,
                use_append_random_significant_words=False,
                use_translations=True,
                use_typos=False,
                use_append_random_date=False,
                use_abbreviations=False,
                use_synonyms=False,
                use_antonyms=False,
            ),
            AugmentationMethods(
                use_deletion=False,
                use_shuffle=False,
                use_append_random_significant_words=False,
                use_translations=False,
                use_typos=True,
                use_append_random_date=False,
                use_abbreviations=False,
                use_synonyms=False,
                use_antonyms=False,
            ),
            AugmentationMethods(
                use_deletion=False,
                use_shuffle=False,
                use_append_random_significant_words=False,
                use_translations=False,
                use_typos=False,
                use_append_random_date=True,
                use_abbreviations=False,
                use_synonyms=False,
                use_antonyms=False,
            ),
            AugmentationMethods(
                use_deletion=False,
                use_shuffle=False,
                use_append_random_significant_words=False,
                use_translations=False,
                use_typos=False,
                use_append_random_date=False,
                use_abbreviations=True,
                use_synonyms=False,
                use_antonyms=False,
            ),
            AugmentationMethods(
                use_deletion=False,
                use_shuffle=False,
                use_append_random_significant_words=False,
                use_translations=False,
                use_typos=False,
                use_append_random_date=False,
                use_abbreviations=False,
                use_synonyms=True,
                use_antonyms=False,
            ),
            AugmentationMethods(
                use_deletion=False,
                use_shuffle=False,
                use_append_random_significant_words=False,
                use_translations=False,
                use_typos=False,
                use_append_random_date=False,
                use_abbreviations=False,
                use_synonyms=False,
                use_antonyms=True,
            ),
            AugmentationMethods(
                use_deletion=True,
                use_shuffle=True,
                use_append_random_significant_words=True,
                use_translations=True,
                use_typos=True,
                use_append_random_date=True,
                use_abbreviations=True,
                use_synonyms=True,
                use_antonyms=True,
                exp_name_override="all"
            ),
            AugmentationMethods(
                use_deletion=False,
                use_shuffle=False,
                use_append_random_significant_words=False,
                use_translations=False,
                use_typos=False,
                use_append_random_date=False,
                use_abbreviations=False,
                use_synonyms=False,
                use_antonyms=False,
                exp_name_override="none"
            ),
            AugmentationMethods(
                use_deletion=True,
                use_shuffle=True,
                use_append_random_significant_words=True,
                use_translations=True,
                use_typos=True,
                use_append_random_date=True,
                use_abbreviations=True,
                use_synonyms=False,
                use_antonyms=False,
                exp_name_override="all_except_synonyms_antonyms"
            ),
            AugmentationMethods(
                use_deletion=True,
                use_shuffle=True,
                use_append_random_significant_words=True,
                use_translations=True,
                use_typos=True,
                use_append_random_date=True,
                use_abbreviations=True,
                use_synonyms=True,
                use_antonyms=False,
                exp_name_override="all_except_antonyms"
            ),
            AugmentationMethods(
                use_deletion=True,
                use_shuffle=True,
                use_append_random_significant_words=False,
                use_translations=True,
                use_typos=True,
                use_append_random_date=False,
                use_abbreviations=False,
                use_synonyms=True,
                use_antonyms=False,
                exp_name_override="all_except_antonyms_dates_abbreviations_append_words"
            ),
        ]
    )

    commands = ""

    for experiment in experiments:
        exp_name = experiment.format_str() + "_" + str(oversampling_factor)
        commands += f"sbatch train.slurm {exp_name} 30\n"

        if exp_name not in [config["name"] for config in ditto_configurations]:
            ditto_configurations.append(
                {
                    "name": exp_name,
                    "task_type": "classification",
                    "vocab": ["0", "1"],
                    "trainset": f"data/synthetic_data/{exp_name}_train.txt",
                    "validset": f"data/synthetic_data/{exp_name}_valid.txt",
                    "testset": "data/goldstandard_test.txt",
                }
            )

        p = multiprocessing.Process(
            target=main,
            args=(
                experiment,
                exp_name,
            ),
        )
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    print(commands)

    with open("configs.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(ditto_configurations, ensure_ascii=False, indent=2))
