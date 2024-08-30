def prepare_arrival_condition(arrival_condition: str, condition_and_repair_record: str):
    prep_arrival_condition = ""

    if arrival_condition is not None:
        prep_arrival_condition = arrival_condition
        if (
            condition_and_repair_record is not None
            and prep_arrival_condition != condition_and_repair_record
        ):
            prep_arrival_condition += "; " + condition_and_repair_record
    elif condition_and_repair_record is not None:
        prep_arrival_condition = condition_and_repair_record

    return prep_arrival_condition
