import random
from columns import (
    Language,
    Title,
)
from columns.augmentation_methods import AugmentationMethods
from columns.title_payloads.append_random_significant_words import (
    append_random_significant_words,
)
from .augment import *


def get_random_equal_titles(
    fetch_from: list,
    flags: AugmentationMethods,
    probablity: float = 0.5,
):
    reference_title = random.choice(fetch_from)

    if isinstance(reference_title, Title):
        title_1 = reference_title.title
        if reference_title.is_antonym:
            title_2 = reference_title.title
        else:
            title_2 = reference_title.corresponding_title

            if flags.use_append_random_significant_words:
                if (
                    reference_title.co_language != Language.Mixed
                    and random.random() < probablity
                ):
                    title_2 = append_random_significant_words(
                        title_2, reference_title.co_language
                    )
                if (
                    reference_title.language != Language.Mixed
                    and random.random() < probablity
                ):
                    title_1 = append_random_significant_words(
                        title_1, reference_title.language
                    )
    else:
        title_1 = reference_title
        title_2 = reference_title

    if flags.use_typos and random.random() < probablity:
        title_1 = introduce_typos(title_1)
    if flags.use_typos and random.random() < probablity:
        title_2 = introduce_typos(title_2)

    if flags.use_shuffle and random.random() < probablity:
        title_1 = shuffle_str(title_1, 0.06)
    if flags.use_shuffle and random.random() < probablity:
        title_2 = shuffle_str(title_2, 0.06)

    if flags.use_deletion and random.random() < probablity:
        title_2 = delete_random_words(title_2, 0.1)

    if random.random() < 0.5:
        return title_1, title_2
    else:
        return title_2, title_1


def get_random_nonequal_titles(
    fetch_from: list,
    flags: AugmentationMethods,
    probablity: float = 0.5,
):
    reference_title_1, reference_title_2 = random.sample(fetch_from, 2)
    title_1 = None
    title_2 = None

    if isinstance(reference_title_2, Title):
        title_2 = reference_title_2.title
        if reference_title_2.is_antonym:
            title_1 = reference_title_2.corresponding_title
            reference_title_1 = None
        if (
            flags.use_append_random_significant_words
            and reference_title_2.language != Language.Mixed
            and random.random() < probablity
        ):
            title_2 = append_random_significant_words(
                title_2, reference_title_2.language
            )
    else:
        title_2 = reference_title_2

    if title_1 is None:
        if isinstance(reference_title_1, Title):
            title_1 = reference_title_1.title
            if (
                flags.use_append_random_significant_words
                and reference_title_1.language != Language.Mixed
                and random.random() < probablity
            ):
                title_1 = append_random_significant_words(
                    title_1, reference_title_1.language
                )
        else:
            title_1 = reference_title_1

    if flags.use_shuffle and random.random() < probablity:
        title_1 = shuffle_str(title_1, 0.05)
    if flags.use_shuffle and random.random() < probablity:
        title_2 = shuffle_str(title_2, 0.05)

    if flags.use_typos and random.random() < probablity:
        title_1 = introduce_typos(title_1)
    if flags.use_typos and random.random() < probablity:
        title_2 = introduce_typos(title_2)

    if flags.use_deletion and random.random() < probablity:
        title_2 = delete_random_words(title_2, 0.1)

    if random.random() < 0.5:
        return title_1, title_2
    else:
        return title_2, title_1
