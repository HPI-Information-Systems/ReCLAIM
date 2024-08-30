import re
from etl import common


def normalize(input: str) -> str | None:
    '''This function normalizes the WCCP number from the input string as it is often not in the correct format.
    You can find some examples in ./test/test_wccp_number.py.
    The output strings are in the format "WIE XXXX" where X is a number.
    '''
    if input is None:
        return input

    input = common.ccp_keywords.remove_ccp_keywords(input)
    # cuts everything before the first occurence of "WIE"
    wie_pattern = input.find("WIE")
    if wie_pattern != -1:
        input = input[wie_pattern:]

    # remove ) if there is no (
    if ")" in input and "(" not in input:
        input = input.replace(")", "")

    # special cases because of OCR faults
    known_special_cases = {
        "Unknown 1 Fcty deda and the Swee": "WIE 6401",
        "2 schofers": "WIE 6624/1-2",
        "WIE 6191/13/9EXIEDLE": "WIE 191/13/9",
    }

    if input in known_special_cases:
        return known_special_cases[input]

    # handle the cases where the input starts with Unknown
    if input.startswith("Unknown"):
        return input

    if input.endswith("-"):
        input = input[:-1]
    if input.endswith('"'):
        input = input[:-1]

    input = input.strip()

    input = input.replace("\n", " ")
    input = input.replace("\r", " ")

    # prepare input to match the regex - exchange numbers and letters the right way
    regex = re.compile(r"W1E")
    input = regex.sub("WIE", input)
    regex = re.compile(r"o/|C/")
    input = regex.sub("0/", input)
    regex = re.compile(r"X8X")
    input = regex.sub("XXX", input)

    # match the wccp number
    regex = re.compile(r"[0-9](?:[+/ ,.-]?[ \(]?(- |/ )?[0-9\)a-z]+)*")
    number_match = regex.search(input)
    suffix = re.split(regex, input, 1)

    if number_match is None:
        return input

    number = number_match.group(0)

    regex = re.compile(r" / ")
    number = regex.sub("/", number)
    output = "WIE " + number
    if suffix[2] != "" and suffix[2] != None:
        output += str(suffix[2])

    return output
