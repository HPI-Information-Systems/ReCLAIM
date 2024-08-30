import json


def parse(input: str | None) -> str | None:
    '''This function parses the object date from the input string in a certain format, which occurs in the objectDate column of the munich dataset.
    ['19. Jhd.', '1801/1900'] -> '19. Jhd.'
    '''

    if input is None:
        return None

    # The input string conceptually is a JSON array, but it uses single quotes instead of double quotes.
    # To handle this, we replace all single quotes with double quotes before parsing the JSON.
    input = input.replace("'", '"')
    date_list = json.loads(input)

    if len(date_list) == 0:
        return None

    return date_list[0]
