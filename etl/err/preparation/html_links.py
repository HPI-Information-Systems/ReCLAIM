import re


def remove(input):
    ''' This function removes the html links from the input string. 
    
    The regex pattern is often found in the objectPostConfiscationHistory field of the err data. '''
    regex = re.compile(
        r"<a target=\'_blank\' *href=\'([\w\s=:.?&\/\-\_%#{}]*)\"?\'?’?>?([\w\s\-,\'éç]*)<\/a>"
    )

    matches = regex.findall(input)

    if matches is None:
        return input

    for match in matches:
        link = match[0]
        display_word = match[1]
        output = display_word + " (" + link + ")"
        input = re.sub(regex, output, input, count=1)

    return input
