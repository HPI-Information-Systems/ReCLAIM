from enum import Enum


class Language(Enum):
    DE = 0
    EN = 1
    Mixed = 2


class Title:
    def __init__(
        self,
        title,
        corresponding_title,
        language: Language,
        co_language: Language,
        is_antonym: bool = False,
    ):
        self.title = title
        self.corresponding_title = corresponding_title
        self.language = language
        self.co_language = co_language
        self.is_antonym = is_antonym


def load_titles_with_correspondence(
    filename: str,
    filename_translated: str,
    language: Language,
    co_language: Language,
    is_antonym: bool = False,
) -> list[Title]:
    titles = open(filename, "r", encoding="utf-16-le").read().splitlines()
    corresponding_titles = (
        open(filename_translated, "r", encoding="utf-16-le").read().splitlines()
    )
    assert len(titles) == len(corresponding_titles)
    titles = [title for title in titles if title != ""]
    for i in range(len(titles) - 1, -1, -1):
        if corresponding_titles[i] == "":
            titles.pop(i)
            corresponding_titles.pop(i)
    return [
        Title(titles[i], corresponding_titles[i], language, co_language, is_antonym)
        for i in range(len(titles))
    ]


def load_titles_simple(filename: str) -> list[str]:
    return open(filename, "r", encoding="utf-16-le").read().splitlines()


titles_with_translation = (
    load_titles_with_correspondence(
        "data/translations/titles_wccp_linz_de.txt",
        "data/translations/titles_wccp_linz_de_to_en.txt",
        Language.DE,
        Language.EN,
    )
    + load_titles_with_correspondence(
        "data/translations/titles_wccp_linz_en.txt",
        "data/translations/titles_wccp_linz_en_to_de.txt",
        Language.EN,
        Language.DE,
    )
    + load_titles_with_correspondence(
        "data/basic/titles_marburg.txt",
        "data/translations/titles_marburg_to_de.txt",
        Language.EN,
        Language.DE,
    )
    + load_titles_with_correspondence(
        "data/basic/titles_err_1.txt",
        "data/translations/titles_err_to_en_1.txt",
        Language.Mixed,
        Language.EN,
    )
)

titles_simple = (
    load_titles_simple("data/basic/titles_err_1.txt")
    + load_titles_simple("data/basic/titles_err_2.txt")
    + load_titles_simple("data/basic/titles_marburg.txt")
    + load_titles_simple("data/basic/titles_wccp_linz.txt")
)

titles_with_synonyms = (
    load_titles_with_correspondence(
        "data/translations/titles_wccp_linz_de.txt",
        "data/synonyms/titles_wccp_linz_de_synonyms.txt",
        Language.DE,
        Language.DE,
    )
    + load_titles_with_correspondence(
        "data/translations/titles_wccp_linz_en.txt",
        "data/synonyms/titles_wccp_linz_en_synonyms.txt",
        Language.EN,
        Language.EN,
    )
    + load_titles_with_correspondence(
        "data/basic/titles_marburg.txt",
        "data/synonyms/titles_marburg_synonyms.txt",
        Language.EN,
        Language.EN,
    )
    + load_titles_with_correspondence(
        "data/translations/titles_marburg_to_de.txt",
        "data/synonyms/titles_marburg_to_de_synonyms.txt",
        Language.DE,
        Language.DE,
    )
    + load_titles_with_correspondence(
        "data/basic/titles_err_1.txt",
        "data/synonyms/titles_err_1_synonyms.txt",
        Language.EN,
        Language.EN,
    )
    + load_titles_with_correspondence(
        "data/translations/titles_err_to_en_1.txt",
        "data/synonyms/titles_err_to_en_1_synonyms.txt",
        Language.EN,
        Language.EN,
    )
    + load_titles_with_correspondence(
        "data/translations/titles_wccp_linz_de_to_en.txt",
        "data/synonyms/titles_wccp_linz_de_to_en_synonyms.txt",
        Language.EN,
        Language.EN,
    )
    + load_titles_with_correspondence(
        "data/translations/titles_wccp_linz_en_to_de.txt",
        "data/synonyms/titles_wccp_linz_en_to_de_synonyms.txt",
        Language.DE,
        Language.DE,
    )
)

titles_with_antonyms = (
    load_titles_with_correspondence(
        "data/translations/titles_wccp_linz_de.txt",
        "data/antonyms/titles_wccp_linz_de_antonyms.txt",
        Language.DE,
        Language.DE,
        True,
    )
    + load_titles_with_correspondence(
        "data/translations/titles_wccp_linz_en.txt",
        "data/antonyms/titles_wccp_linz_en_antonyms.txt",
        Language.EN,
        Language.EN,
        True,
    )
    + load_titles_with_correspondence(
        "data/translations/titles_wccp_linz_de_to_en.txt",
        "data/antonyms/titles_wccp_linz_de_to_en_antonyms.txt",
        Language.EN,
        Language.EN,
        True,
    )
    + load_titles_with_correspondence(
        "data/translations/titles_wccp_linz_en_to_de.txt",
        "data/antonyms/titles_wccp_linz_en_to_de_antonyms.txt",
        Language.DE,
        Language.DE,
        True,
    )
    + load_titles_with_correspondence(
        "data/basic/titles_err_1.txt",
        "data/antonyms/titles_err_1_antonyms.txt",
        Language.EN,
        Language.EN,
        True,
    )
    + load_titles_with_correspondence(
        "data/translations/titles_err_to_en_1.txt",
        "data/antonyms/titles_err_to_en_1_antonyms.txt",
        Language.EN,
        Language.EN,
        True,
    )
    + load_titles_with_correspondence(
        "data/basic/titles_marburg.txt",
        "data/antonyms/titles_marburg_antonyms.txt",
        Language.EN,
        Language.EN,
        True,
    )
    + load_titles_with_correspondence(
        "data/translations/titles_marburg_to_de.txt",
        "data/antonyms/titles_marburg_to_de_antonyms.txt",
        Language.DE,
        Language.DE,
        True,
    )
    + load_titles_with_correspondence(
        "data/basic/titles_munich.txt",
        "data/antonyms/titles_munich_antonyms.txt",
        Language.EN,
        Language.EN,
        True,
    )
)

DATASET_SIZE = (
    len(titles_simple)
    + len(titles_with_translation)
    + len(titles_with_synonyms)
    + len(titles_with_antonyms)
)
