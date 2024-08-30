from enum import Enum
import random


def shuffle_str(input: str, swap_percentage: float = 0.4) -> str:
    """
    Returns a copy of the input string with some words swapped around.
    Each word has a swap_percentage chance of being swapped with another word.
    """

    word_list = input.split()
    num_words = len(word_list)
    if num_words < 2:
        return input
    for _ in range(num_words):
        if random.random() < swap_percentage:
            index1, index2 = random.sample(range(num_words), 2)
            word_list[index1], word_list[index2] = word_list[index2], word_list[index1]
    
    return " ".join(word_list)


def delete_random_words(input: str, delete_percentage: float = 0.06) -> str:
    """
    Returns a copy of the input string with random words deleted from it.
    Each word has a delete_percentage chance of being deleted.
    """

    word_list = input.split()
    num_words = len(word_list)
    for word in word_list:
        if random.random() < delete_percentage:
            word_list.remove(word)

    return " ".join(word_list)


def introduce_typos(input: str, typo_percentage: float = 0.06) -> str:
    """
    Returns a copy of the input string with typos introduced in it
    """

    typoed_word_list = []
    for word in input.split():
        if random.random() < typo_percentage:
            typoed_word = list(word)
            random_index = random.randint(0, len(typoed_word) - 1)
            typoed_word[random_index] = random.choice("abcdefghijklmnopqrstuvwxyz")
            typoed_word_list.append("".join(typoed_word))
        else:
            typoed_word_list.append(word)
    return " ".join(typoed_word_list)


class DateTypes(Enum):
    DIGIT_RANGE = 1  # (1920-1938)
    DIGIT_SINGLE = 2  # (1934)
    VAGUE_RANGE = 3  # (Mitte 1800 - Ende 1880er)
    VAGUE_SINGLE = 4  # (Mitte 1840er)
    VAGUE_CENTURY = 5  # (19. Jhrdt.)


def append_random_date(input: str) -> str:
    """
    Returns a copy of the input string with a random date appended to it
    """

    range_words = ['Anfang ', 'Mitte ', 'Ende ', '']
    century_words = ['Jahrhundert', 'Jhrdt.', 'Jhr.']

    date_type = random.choice(list(DateTypes))
    match date_type:
        case DateTypes.DIGIT_RANGE:
            return f"{input} ({random.randint(1800, 1850)}-{random.randint(1860, 1950)})"
        case DateTypes.DIGIT_SINGLE:
            return f"{input} ({random.randint(1800, 1950)})"
        case DateTypes.VAGUE_RANGE:
            return f"{input} ({random.choice(range_words)}{random.randint(180, 184)}0er - {random.choice(range_words)}{random.randint(185, 190)}0er)"
        case DateTypes.VAGUE_SINGLE:
            return f"{input} ({random.choice(range_words)}{random.randint(185, 190)}0er)"
        case DateTypes.VAGUE_CENTURY:
            return f"{input} ({random.choice(range_words)}{random.randint(18, 20)}. {random.choice(century_words)})"

