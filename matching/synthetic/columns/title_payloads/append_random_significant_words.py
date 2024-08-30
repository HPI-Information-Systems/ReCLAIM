from .. import Language, titles_with_translation
import random

# Extract all words from each title array which have at least SIGNIFICANT_MIN_LEN characters
SIGNIFICANT_MIN_LEN = 5
title_significant_words_de = []
title_significant_words_en = []

for t in titles_with_translation:
    for word in t.title.split():
        if len(word) >= SIGNIFICANT_MIN_LEN:
            if t.language == Language.DE:
                title_significant_words_de.append(word)
            else:
                title_significant_words_en.append(word)


def append_random_significant_words(title: str, language: Language) -> str:
    # Choose between 0 and 3 words from the significant words array
    if language == Language.DE:
        return " ".join(
            [title] + random.sample(title_significant_words_en, random.randint(0, 3))
        )
    elif language == Language.EN:
        return " ".join(
            [title] + random.sample(title_significant_words_de, random.randint(0, 3))
        )
    else:
        raise ValueError("Language not supported:", language)
