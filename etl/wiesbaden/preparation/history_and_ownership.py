import json

from etltools.cache import JsonCache
from wiesbaden.preparation.event_extraction.prepare_arrival_condition import (
    prepare_arrival_condition,
)


def get_event_chain(
    history_and_ownership: str,
    depot_possessor: str,
    depot_number: str,
    arrival_condition: str,
    condition_and_repair_record: str,
    arrival_date: str,
    exit_date: str,
    cache: JsonCache,
) -> list[dict[str, str]] | None:
    
    prep_arrival_condition = prepare_arrival_condition(
        arrival_condition, condition_and_repair_record
    )

    cache_key = json.dumps(
        {
            "history_and_ownership": history_and_ownership,
            "depot_possessor": depot_possessor,
            "depot_number": depot_number,
            "arrival_condition": prep_arrival_condition,
            "arrival_date": arrival_date,
            "exit_date": exit_date,
        }
    )

    return cache.get(cache_key)
