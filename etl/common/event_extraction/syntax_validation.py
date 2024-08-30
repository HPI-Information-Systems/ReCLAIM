import json


def get_parsing_error(json_error: str) -> dict:
    return {
        "identifier": "JSON_PARSING_ERROR",
        "error": f"Error parsing JSON: {json_error}",
    }


def get_invalid_event_type_error(event_type: str) -> dict:
    return {
        "identifier": "INVALID_EVENT_TYPE",
        "error": f"Event type '{event_type}' is not valid.",
    }


def get_invalid_event_key_error(event_key: str, event_type: str) -> dict:
    return {
        "identifier": "INVALID_EVENT_KEY",
        "error": f"Key '{event_key}' is not valid for event type '{event_type}'",
    }


def get_missing_event_key_error(event_key: str, event_type: str) -> dict:
    return {
        "identifier": "MISSING_EVENT_KEY",
        "error": f"Key '{event_key}' is missing for event type '{event_type}'.",
    }


def validate_event_syntax(json_result: str, event_schema: list[dict]) -> dict:
    """
    This function is used to validate the syntax of the produced LLM output and to repair it if possible.
    """

    try:
        parsed_result = json.loads(json_result)
        event_chain = parsed_result["structured"]
    except Exception as e:
        return {"success": False, "event_errors": [get_parsing_error(str(e))]}

    if not isinstance(event_chain, list):
        return {
            "success": False,
            "event_errors": [get_parsing_error("Event chain is not a list.")],
        }

    valid_event_types = [key for key in event_schema.keys()]
    event_errors = []

    for event in event_chain:
        if event["type"] not in valid_event_types:
            # This is not relevant to fix for the clean event chain
            event_errors.append(get_invalid_event_type_error(event["type"]))

        schema_event_type = event_schema[event["type"]]
        event_keys_to_delete = []

        for key in event.keys():
            if key != "type" and key not in schema_event_type["fields"]:
                # Remove the invalid key from that event
                event_keys_to_delete.append(key)
                event_errors.append(get_invalid_event_key_error(key, event["type"]))

            if event.get(key, None) is not None and type(event[key]) != str:
                # Use the casted event attribute instead
                event[key] = str(event[key])
                event_errors.append(
                    get_parsing_error(
                        f"invalid type {type(event[key])} for key {key} in event type {event['type']}"
                    )
                )

        for key in event_keys_to_delete:
            del event[key]

        for key in schema_event_type["fields"]:
            if key not in event.keys():
                # Insert a None-attribute for that key
                event[key] = None
                event_errors.append(get_missing_event_key_error(key, event["type"]))

    if len(event_errors) > 0:
        return {
            "success": False,
            "event_errors": event_errors,
            "clean_event_chain": event_chain,
        }

    return {"success": True, "event_errors": [], "clean_event_chain": event_chain}
