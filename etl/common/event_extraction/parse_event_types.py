def parse_event_types(event_types: dict) -> str:
    """
    This function converts the JSON decoded event types into a string for inclusion in the prompt.
    """

    event_types_formatted = ""
    for event_type in event_types.keys():
        event_types_formatted += f"""

    {event_type}: {{"""
        for attribute in event_types[event_type]["fields"].keys():
            event_types_formatted += f"""
        {attribute}: {event_types[event_type]["fields"][attribute]["type"]} ({event_types[event_type]["fields"][attribute]["description"]}),"""
        event_types_formatted += f"""
    }},"""

    return event_types_formatted


def parse_event_descriptions(event_types: dict) -> str:
    """
    This function converts the JSON decoded event type descriptions (semantic and trigger words) into a string for inclusion in the prompt.
    """

    event_descriptions = ""
    for event_type in event_types.keys():
        event_descriptions += f"""- {event_type}:
    - {event_types[event_type]['semantic']}
    - trigger words: {", ".join(event_types[event_type]['trigger_words'])}\n\n"""

    return event_descriptions
