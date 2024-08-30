import random
from deepl import Language
from ..gpt.mutually_exclusive_man import *
from ..gpt.mutually_exclusive_woman import *
from ..gpt.mutually_exclusive_objects import *
from ..gpt.similar_nonmatches import *

def introduce_nonequal_adjectives(title: str, language: Language) -> tuple[str, str]:
    if language == Language.DE:
        if "Frau" in title:
            mutually_exclusive_set = random.choice(mutually_exlcusive_groups_woman_de)
            replacement_1, replacement_2 = random.sample(mutually_exclusive_set, 2)
            return title.replace("Frau", replacement_1), title.replace(
                "Frau", replacement_2
            )
        elif "Mannes" in title:
            mutually_exclusive_set = random.choice(mutually_exlcusive_groups_man_de)
            replacement_1, replacement_2 = random.sample(mutually_exclusive_set, 2)
            return title.replace("Mannes", replacement_1), title.replace(
                "Mannes", replacement_2
            )
        elif "Mann" in title:
            mutually_exclusive_set = random.choice(mutually_exlcusive_groups_man_de)
            replacement_1, replacement_2 = random.sample(mutually_exclusive_set, 2)
            return title.replace("Mann", replacement_1), title.replace(
                "Mann", replacement_2
            )
        else:
            return None, None
    elif language == Language.EN:
        if "woman" in title:
            mutually_exclusive_set = random.choice(mutually_exlcusive_groups_woman_en)
            replacement_1, replacement_2 = random.sample(mutually_exclusive_set, 2)
            replacement_1 = replacement_1.replace("Woman", "woman")
            replacement_2 = replacement_2.replace("Woman", "woman")
            return title.replace("woman", replacement_1), title.replace(
                "woman", replacement_2
            )
        elif "Woman" in title:
            mutually_exclusive_set = random.choice(mutually_exlcusive_groups_woman_en)
            replacement_1, replacement_2 = random.sample(mutually_exclusive_set, 2)
            return title.replace("Woman", replacement_1), title.replace(
                "Woman", replacement_2
            )
        elif "man" in title:
            mutually_exclusive_set = random.choice(mutually_exlcusive_groups_man_en)
            replacement_1, replacement_2 = random.sample(mutually_exclusive_set, 2)
            replacement_1 = replacement_1.replace("Man", "man")
            replacement_2 = replacement_2.replace("Man", "man")
            return title.replace("man", replacement_1), title.replace(
                "man", replacement_2
            )
        elif "Man" in title:
            mutually_exclusive_set = random.choice(mutually_exlcusive_groups_man_en)
            replacement_1, replacement_2 = random.sample(mutually_exclusive_set, 2)
            return title.replace("Man", replacement_1), title.replace(
                "Man", replacement_2
            )
        else:
            return None, None
    else:
        raise ValueError("Language not supported:", language)
