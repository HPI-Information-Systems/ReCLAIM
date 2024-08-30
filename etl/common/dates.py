from datetime import datetime


def german_to_iso(date_string: str | None) -> str | None:
    ''' Convert a German date string to an ISO date string. '''
    if date_string is None:
        return None

    return datetime.strptime(date_string, "%d.%m.%Y").isoformat()
