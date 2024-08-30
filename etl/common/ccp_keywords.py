import os
import re

# all keywords in this arrays will be filtered and removed from the value
# The keywords in this array will be filtered out in upper and lower case
property_cards_keywords_both_cases = [
    "PROPERTY CARD-ART",
    "PROPERTY CARD ART",
    "DEPOT NO",
    "DEPOT CAT.",
    "MEASUREMENTS",
    "LOCATION:",
    "LOCATION",
    "DEPOT POSSESSOR",
    "COPIES OF CARD",
    "CLAIM NO",
    "OTHER PHOTOS",
    "WEIGHT",
    "BIBLIOGRAPHY",
    "IDENTIFYING MARKS",
    "FOR OFFICE USE",
    "FOR OFFICE",
    "CONDITION AND REPAIR RECORD",
    "EXIT DATE",
    "CATALOG NO",
    "ARRIVAL DATE",
    "ARRIVAL CONDITION",
    "HISTORY AND OWNERSHIP",
    "PROPERTY CARD",
    "PRESUMED OWNER",
    "OFFICE USE",
    "FOR OFFICE USE",
    "FOR:OFFICE USE",
    "FOR:OFFICE",
    "CARD-ART",
    "POSSESSOR",
    "EXIT DATE",
    "INV. NO",
    "NEG. NO",
    "CAT. NO",
    "CLASSIFICATION",
]
# The keywords in this array will be filtered out in upper case only. This is done to avoid removing words that are not keywords e.g. soldaten contains date
property_cards_keywords_only_uppercase = [
    "DATE",
    "MATERIAL",
    "PROPERTY",
    "DESCRIPTION",
    "OFFICE",
    "AUTHOR",
    "SUBJECT",
    "ARRIVAL",
    "OF CARD",
    "DEPOT",
    "CARD",
]
# create regex from the keyowrdarrays
regex_pattern_both = "|".join(
    re.escape(keyword) + r"(?:\:)?" for keyword in property_cards_keywords_both_cases
)
regex_both = re.compile(regex_pattern_both, re.IGNORECASE)
regex_pattern_only_upper = "|".join(
    re.escape(keyword) + r"(?:\:)?"
    for keyword in property_cards_keywords_only_uppercase
)
regex_only_upper = re.compile(regex_pattern_only_upper)
# global variable to store the removed words for statistics
word_counts = {}


def remove_ccp_keywords(value: str) -> str:
    ''' In the CCP data, there are some OCR errors that lead to keywords like "PROPERTY CARD-ART" being included in the data. This function removes these keywords from the data. '''
    if value is None:
        return value
    keyword = re.findall(regex_both, value)
    if keyword:
        for word in keyword:
            value = value.replace(word, "")

            if word in word_counts:
                word_counts[word] += 1
            else:
                word_counts[word] = 1

    keyword = re.findall(regex_only_upper, value)

    if keyword:
        for word in keyword:
            value = value.replace(word, "")

            if word in word_counts:
                word_counts[word] += 1
            else:
                word_counts[word] = 1

    return value



def print_removed_words_wccp():
    ''' this method shows the count of the words that are removed from the Wiesbaden data and writes them to a file. '''
    sorted_word_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    with open(
        os.path.join(
            os.path.dirname(__file__), "..", "wiesbaden/preparation", "wccp_removed_words.txt"
        ),
        "w",
    ) as file:
        file.write(
            "This file contains all keywords that are removed from the WCCP data with the count of their occurences\n\n"
        )
        for word, count in sorted_word_counts:
            file.write(f"{word}: {count}\n")

        file.write("\n\nTotal removed words: " + str(sum(word_counts.values())))


def print_removed_words_marburg():
    ''' this method shows the count of the words that are removed from the Marburg data and writes them to a file. '''
    sorted_word_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    with open(
        os.path.join(
            os.path.dirname(__file__), "..", "marburg/preparation", "marburg_removed_words.txt"
        ),
        "w",
    ) as file:
        file.write(
            "This file contains all keywords that are removed from the marburg data with the count of their occurences\n\n"
        )
        for word, count in sorted_word_counts:
            file.write(f"{word}: {count}\n")

        file.write("\n\nTotal removed words: " + str(sum(word_counts.values())))
