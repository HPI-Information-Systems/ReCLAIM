from etltools.record import Record
from etltools.entity import Entity
from rdflib import XSD


def set_event_related_entity(
    event_entity: Entity,
    related_entity_data: str | list[str],
    ca_id: str,
    event_idx: str,
    relation_name: str,
    related_entity_type: str,
    related_entity_attribute_name: str,
    record: Record,
    derived_using: list[str],
) -> None:
    related_entity_list = (
        related_entity_data
        if type(related_entity_data) == list[str]
        else [related_entity_data]
    )
    for idx, related_entity_attribute_value in enumerate(related_entity_list):
        related_entity = Entity(
            identifier=ca_id
            + "_event_"
            + event_idx
            + "_"
            + relation_name
            + "_"
            + str(idx),
            base_type=related_entity_type,
            derived_from=record,
        )
        related_entity.literal(
            attribute=related_entity_attribute_name,
            value=related_entity_attribute_value,
            derived_using=derived_using,
        )
        event_entity.related(via=relation_name, with_entity=related_entity)


def set_general_attributes(
    ca_id: str,
    event: Entity,
    event_idx: int,
    record: Record,
    derived_using: list[str],
    event_data: dict[str, str],
) -> None:
    event.literal(
        attribute="description",
        value=event_data["description"],
        derived_using=derived_using,
    )

    event.literal(
        attribute="relativeOrder",
        value=event_idx,
        derived_using=derived_using,
        datatype=XSD.integer,
    )

    event.literal(
        attribute="date", value=event_data["date"], derived_using=derived_using
    )

    event.literal(
        attribute="physicalDescription",
        value=event_data["physical_description"],
        derived_using=derived_using,
    )

    if event_data["with_involvement_of"] is not None:
        set_event_related_entity(
            event,
            event_data["with_involvement_of"],
            ca_id,
            event_idx,
            "withInvolvementOf",
            "Person",
            "name",
            record,
            derived_using,
        )


def set_transfer_attributes(
    ca_id: str,
    event: Entity,
    event_idx: int,
    record: Record,
    derived_using: list[str],
    event_data: dict[str, str],
) -> None:
    set_general_attributes(ca_id, event, event_idx, record, derived_using, event_data)

    event.literal(
        attribute="departureDate",
        value=event_data["departure_date"],
        derived_using=derived_using,
    )

    event.literal(
        attribute="arrivalDate",
        value=event_data["arrival_date"],
        derived_using=derived_using,
    )

    event.literal(
        attribute="physicalDescriptionBefore",
        value=event_data["physical_description_before"],
        derived_using=derived_using,
    )

    event.literal(
        attribute="physicalDescriptionAfter",
        value=event_data["physical_description_after"],
        derived_using=derived_using,
    )

    if event_data["from_location"] is not None:
        set_event_related_entity(
            event,
            event_data["from_location"],
            ca_id,
            event_idx,
            "fromLocation",
            "Location",
            "description",
            record,
            derived_using,
        )

    if event_data["to_location"] is not None:
        set_event_related_entity(
            event,
            event_data["to_location"],
            ca_id,
            event_idx,
            "toLocation",
            "Location",
            "description",
            record,
            derived_using,
        )

    if event_data["by_legal_entity"] is not None:
        set_event_related_entity(
            event,
            event_data["by_legal_entity"],
            ca_id,
            event_idx,
            "byLegalEntity",
            "LegalEntity",
            "name",
            record,
            derived_using,
        )

    if event_data["identified_by"] is not None:
        set_event_related_entity(
            event,
            event_data["identified_by"],
            ca_id,
            event_idx,
            "identifiedBy",
            "LegalEntity",
            "name",
            record,
            derived_using,
        )

    if event_data["possessor_before"] is not None:
        set_event_related_entity(
            event,
            event_data["possessor_before"],
            ca_id,
            event_idx,
            "possessorBefore",
            "LegalEntity",
            "name",
            record,
            derived_using,
        )

    if event_data["possessor_after"] is not None:
        set_event_related_entity(
            event,
            event_data["possessor_after"],
            ca_id,
            event_idx,
            "possessorAfter",
            "LegalEntity",
            "name",
            record,
            derived_using,
        )


def set_deposition_event_attributes(
    ca_id: str,
    event: Entity,
    event_idx: int,
    record: Record,
    derived_using: list[str],
    event_data: dict[str, str],
) -> None:
    set_general_attributes(ca_id, event, event_idx, record, derived_using, event_data)

    event.literal(
        attribute="depotNumber",
        value=event_data["depot_number"],
        derived_using=derived_using,
    )

    if event_data["at_location"] is not None:
        set_event_related_entity(
            event,
            event_data["at_location"],
            ca_id,
            event_idx,
            "atLocation",
            "Location",
            "description",
            record,
            derived_using,
        )

    if event_data["deposited_by"] is not None:
        set_event_related_entity(
            event,
            event_data["deposited_by"],
            ca_id,
            event_idx,
            "depositedBy",
            "LegalEntity",
            "name",
            record,
            derived_using,
        )

    if event_data["possessor"] is not None:
        set_event_related_entity(
            event,
            event_data["possessor"],
            ca_id,
            event_idx,
            "possessor",
            "LegalEntity",
            "name",
            record,
            derived_using,
        )

    if event_data["collected_in"] is not None:
        set_event_related_entity(
            event,
            event_data["collected_in"],
            ca_id,
            event_idx,
            "collectedIn",
            "Collection",
            "name",
            record,
            derived_using,
        )


def set_confiscation_event_attributes(
    ca_id: str,
    event: Entity,
    event_idx: int,
    record: Record,
    derived_using: list[str],
    event_data: dict[str, str],
) -> None:
    set_general_attributes(ca_id, event, event_idx, record, derived_using, event_data)

    if event_data["at_location"] is not None:
        set_event_related_entity(
            event,
            event_data["at_location"],
            ca_id,
            event_idx,
            "atLocation",
            "Location",
            "description",
            record,
            derived_using,
        )

    if event_data["from_legal_entity"] is not None:
        set_event_related_entity(
            event,
            event_data["from_legal_entity"],
            ca_id,
            event_idx,
            "fromLegalEntity",
            "LegalEntity",
            "name",
            record,
            derived_using,
        )

    if event_data["from_collection"] is not None:
        set_event_related_entity(
            event,
            event_data["from_collection"],
            ca_id,
            event_idx,
            "fromCollection",
            "Collection",
            "name",
            record,
            derived_using,
        )

    if event_data["by_legal_entity"] is not None:
        set_event_related_entity(
            event,
            event_data["by_legal_entity"],
            ca_id,
            event_idx,
            "byLegalEntity",
            "LegalEntity",
            "name",
            record,
            derived_using,
        )


def set_acquisition_event_attributes(
    ca_id: str,
    event: Entity,
    event_idx: int,
    record: Record,
    derived_using: list[str],
    event_data: dict[str, str],
) -> None:
    set_general_attributes(ca_id, event, event_idx, record, derived_using, event_data)

    event.literal(
        attribute="acquisitionCost",
        value=event_data["acquisition_cost"],
        derived_using=derived_using,
    )

    if event_data["at_location"] is not None:
        set_event_related_entity(
            event,
            event_data["at_location"],
            ca_id,
            event_idx,
            "atLocation",
            "Location",
            "description",
            record,
            derived_using,
        )

    if event_data["from_legal_entity"] is not None:
        set_event_related_entity(
            event,
            event_data["from_legal_entity"],
            ca_id,
            event_idx,
            "fromLegalEntity",
            "LegalEntity",
            "name",
            record,
            derived_using,
        )

    if event_data["from_collection"] is not None:
        set_event_related_entity(
            event,
            event_data["from_collection"],
            ca_id,
            event_idx,
            "fromCollection",
            "Collection",
            "name",
            record,
            derived_using,
        )

    if event_data["by_legal_entity"] is not None:
        set_event_related_entity(
            event,
            event_data["by_legal_entity"],
            ca_id,
            event_idx,
            "byLegalEntity",
            "LegalEntity",
            "name",
            record,
            derived_using,
        )

    if event_data["through_legal_entity"] is not None:
        set_event_related_entity(
            event,
            event_data["through_legal_entity"],
            ca_id,
            event_idx,
            "throughLegalEntity",
            "LegalEntity",
            "name",
            record,
            derived_using,
        )


def create_event(
    ca_id: str,
    record: Record,
    derived_using: list[str],
    event_data: dict[str, str],
    event_idx: int,
) -> Entity:
    event = Entity(
        identifier=ca_id + "_event_" + event_idx,
        base_type=str(event_data["type"]).split("_")[0].capitalize() + "Event",
        derived_from=record,
    )

    if event_data["type"] == "transfer_event":
        set_transfer_attributes(
            ca_id, event, event_idx, record, derived_using, event_data
        )
    elif event_data["type"] == "deposition_event":
        set_deposition_event_attributes(
            ca_id, event, event_idx, record, derived_using, event_data
        )
    elif event_data["type"] == "confiscation_event":
        set_confiscation_event_attributes(
            ca_id, event, event_idx, record, derived_using, event_data
        )
    elif event_data["type"] == "acquisition_event":
        set_acquisition_event_attributes(
            ca_id, event, event_idx, record, derived_using, event_data
        )

    return event
