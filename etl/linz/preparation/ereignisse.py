def parse_event_list(events_str: str) -> list[tuple[int, str, str]]:
    ''' This function parses the events string and returns a list of tuples with the event index, event type and event description  
    ''' 
    event_lines: list[str] = events_str.split("<br>")
    event_lines[0] = event_lines[0][5:]  # Remove "\n			"
    events = []

    for index, line in enumerate(event_lines):
        if len(line.strip()) == 0:
            continue

        raw_event_type = line.split(":")[0].strip()

        if len(raw_event_type) == 0:
            continue

        event_type = normalize_event_type(raw_event_type)
        event_description = line.split(":")[1].strip()

        events.append((index, event_type, event_description))

    return events


def normalize_event_type(event_type: str) -> str:
    '''
     We need to map each of these possible typos to the correct event type Correct types: {'Vorbesitzer',
    'Einlieferung', 'Verbleib', 'Beschlagnahmung', 'Restitution', 'Zwangsverkauf'} All types, including typos:
     'Restitution', 'Einlieferer', 'Verbeib', 'Zwangsverkauf', 'Zwangsverakuf', 'Vobesitzer', 'Verbleib',
     'Beschlagnahmuing', 'Einlieferung', 'Beschlagnahung', 'Beschlagnahmumg', 'Restitutiton', 'Einlieggnahmumg',
     'Restitutiton', 'Einliegerung', 'Beschlagnahmung', 'Vorbsitzer', 'Vorbesiter', 'Vorbesitzer'
    ''' 

    if event_type in ["Restitution", "Restitutiton"]:
        return "Restitution"
    elif event_type in [
        "Einlieferer",
        "Einlieferung",
        "Einlieggnahmumg",
        "Einliegerung",
    ]:
        return "Einlieferung"
    elif event_type in ["Verbeib", "Verbleib"]:
        return "Verbleib"
    elif event_type in ["Zwangsverkauf", "Zwangsverakuf"]:
        return "Zwangsverkauf"
    elif event_type in ["Vobesitzer", "Vorbesiter", "Vorbesitzer", "Vorbsitzer"]:
        return "Vorbesitzer"
    elif event_type in [
        "Beschlagnahmuing",
        "Beschlagnahung",
        "Beschlagnahmumg",
        "Beschlagnahmung",
    ]:
        return "Beschlagnahmung"
    else:
        raise Exception("Unknown event type: " + event_type)
