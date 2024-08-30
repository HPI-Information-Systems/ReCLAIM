import random
from .augment import *

persons = open("data/basic/persons.txt", "r", encoding="utf-8").read().splitlines()


def get_random_equal_persons(
    use_deletion: bool = False,
    use_shuffle: bool = False,
    use_abbreviations: bool = False,
    use_append_random_date: bool = False,
    use_typos: bool = False,
    probablity: float = 0.5,
):
    reference_person = random.choice(persons)
    person_1 = reference_person
    person_2 = reference_person

    if use_deletion and random.random() < probablity:
        person_1 = delete_random_words(person_1)

    if use_typos and random.random() < probablity:
        person_1 = introduce_typos(person_1)

    if use_append_random_date and random.random() < probablity:
        person_1 = append_random_date(person_1)

    if use_abbreviations and random.random() < probablity:
        person_2 = abbreviate_str(person_2)

    if use_shuffle and random.random() < probablity:
        person_2 = shuffle_str(person_2)

    return person_1, person_2


def get_random_nonequal_persons(
    use_deletion: bool = False,
    use_shuffle: bool = False,
    use_abbreviations: bool = False,
    use_append_random_date: bool = False,
    use_typos: bool = False,
    probablity: float = 0.5,
):
    person_1, person_2 = random.sample(persons, 2)
    assert person_1 != person_2

    if use_deletion and random.random() < probablity:
        person_1 = delete_random_words(person_1)

    if use_typos and random.random() < probablity:
        person_1 = introduce_typos(person_1)

    if use_append_random_date and random.random() < probablity:
        person_1 = append_random_date(person_1)

    if use_abbreviations and random.random() < probablity:
        person_2 = abbreviate_str(person_2)

    if use_shuffle and random.random() < probablity:
        person_2 = shuffle_str(person_2)

    return person_1, person_2


def abbreviate_str(input: str, abbreviate_percentage: float = 0.5) -> str:
    """
    Returns a copy of the input string with random abbreviated words
    """

    word_list = input.split()
    num_words = len(word_list)
    num_words_to_abbreviate = int(num_words * abbreviate_percentage)
    if num_words_to_abbreviate == 0:
        return input
    words_to_abbreviate = random.sample(word_list, num_words_to_abbreviate)
    for word in words_to_abbreviate:
        if len(word) < 3:
            continue
        if word[0] == "(" and word[-1] == ")":
            word_list[word_list.index(word)] = "(" + word[1:2] + ".)"
        else:
            word_list[word_list.index(word)] = word[:1] + "."
    return " ".join(word_list)
