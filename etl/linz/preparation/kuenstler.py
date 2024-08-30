import re


def extract_names(input_str: str) -> list[str]:
    '''Extracts the names from the input string'''
    two_names = re.match(r"([^(),]+), (.+) \(.*\)", input_str)
    if two_names is not None:
        return [two_names.groups()[0], two_names.groups()[1]]

    one_name = re.match(r"(.+) \(.*\)", input_str)
    if one_name is not None:
        return [one_name.groups()[0]]

    return []


def extract_years(input_str: str) -> list[str]:
    '''Extracts the years from the input string'''
    # handle cases like (16. Jhrdt. (?)) or (16. Jhrdt. (um))
    if input_str.endswith("(?))"):
        date_substring: str = "(" + input_str.split(" (")[-2] + " (?))"
    elif input_str.endswith("(um))"):
        date_substring: str = "(" + input_str.split(" (")[-2] + " (um))"
    else:
        date_substring: str = "(" + input_str.split(" (")[-1]

    match = re.match(r"\((.*)-(.*)\)", date_substring)

    if match:
        return [match.groups()[0].strip(), match.groups()[1].strip()]

    return [date_substring.strip()]
