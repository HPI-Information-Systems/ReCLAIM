from common.event_extraction.parse_event_types import (
    parse_event_types,
    parse_event_descriptions,
)


def build_prompt(event_types: dict, examples: str):
    """
    This function constructs the wccp prompt with the event types and examples.
    """

    with open("./resources/prompt.txt") as prompt_src:
        prompt = prompt_src.format(
            event_types=parse_event_types(event_types),
            event_descriptions=parse_event_descriptions(event_types),
            examples=examples,
        )

    return prompt
