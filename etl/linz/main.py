from __future__ import annotations
from linz import preparation
from etl import etltools, common


from rdflib import XSD

from etl import etltools


def create_record(row, index) -> etltools.Record:
    return etltools.Record(
        source_id="linz", collection_id="card", record_id=str(index), data=row
    )


def create_cultural_asset(record: etltools.Record) -> etltools.Entity:
    assert record["sammlung"] == "Linzer Sammlung"

    cultural_asset = etltools.Entity(
        identifier=record["laufNr"], base_type="CulturalAsset", derived_from=record
    )

    cultural_asset.literal(attribute="title", derived_using="titel")
    cultural_asset.literal(attribute="measurements", derived_using="maße")
    cultural_asset.literal(attribute="munichNumber", derived_using="müNr")
    cultural_asset.literal(attribute="linzNumber", derived_using="linzNr")
    cultural_asset.literal(attribute="creationDate", derived_using="datierung")

    cultural_asset.related(via="createdBy", with_entity=create_creator_person(record))
    cultural_asset.related(via="depictedInImage", with_entity=create_image(record))

    relate_classifications_and_materials(cultural_asset, record, "objekttyp")
    relate_classifications_and_materials(cultural_asset, record, "materialTechnik")

    create_events(record, cultural_asset)

    return cultural_asset


def create_creator_person(record: etltools.Record) -> etltools.Entity | None:
    creator_string: str = record["künstler"]

    if creator_string is None:
        return None

    creator = etltools.Entity(
        identifier=record["laufNr"] + "_creator",
        base_type="Person",
        derived_from=record,
    )

    # Extract names
    names: list[str] = preparation.kuenstler.extract_names(creator_string)

    if len(names) == 1:
        creator.literal(attribute="pseudonym", value=names[0], derived_using="künstler")
    elif len(names) == 2:
        creator.literal(attribute="lastName", value=names[0], derived_using="künstler")
        creator.literal(attribute="firstName", value=names[1], derived_using="künstler")
    else:
        raise ValueError(
            f"Could not extract artist name from creator string: {creator_string}"
        )

    years = preparation.kuenstler.extract_years(creator_string)

    if len(years) == 1:
        creator.literal(attribute="lifetime", value=years[0], derived_using="künstler")
    elif len(years) == 2:
        creator.literal(attribute="birthDate", value=years[0], derived_using="künstler")
        creator.literal(attribute="deathDate", value=years[1], derived_using="künstler")
    else:
        raise ValueError(
            f"Could not extract years from creator string: {creator_string}"
        )

    return creator


def create_events(record: etltools.Record, cultural_asset: etltools.Entity):
    events = preparation.ereignisse.parse_event_list(record["ereignisse"])

    # these two event types will be stored as comma-delimited strings directly on the cultural asset
    pre_confiscation_history_descriptions = []
    current_remain_descriptions = []

    event_entity_types = {
        "Einlieferung": "TransferEvent",
        "Zwangsverkauf": "AcquisitionEvent",  # ForcedSaleEvent
        "Beschlagnahmung": "ConfiscationEvent",
        "Restitution": "TransferEvent",  # This should be a RestitutionEvent, as soon as this is supported in frontend
    }

    for index, event_type, event_description in events:
        if event_type == "Vorbesitzer":
            pre_confiscation_history_descriptions.append(event_description)
            continue

        if event_type == "Verbleib":
            current_remain_descriptions.append(event_description)
            continue

        if event_type not in event_entity_types:
            raise ValueError(f"Unknown event type at index {str(index)}: {event_type}")

        event = etltools.Entity(
            identifier=record["laufNr"] + "_event" + str(index),
            base_type=event_entity_types[event_type],
            derived_from=record,
        )
        event.literal(
            attribute="relativeOrder",
            value=index,
            derived_using="ereignisse",
            datatype=XSD.integer,
        )
        event.literal(
            attribute="description", value=event_description, derived_using="ereignisse"
        )
        cultural_asset.related(
            via="affectedCulturalAsset", with_entity=event, inverse=True
        )

    if len(pre_confiscation_history_descriptions) > 0:
        cultural_asset.literal(
            attribute="preConfiscationHistoryDescription",
            value=", ".join(pre_confiscation_history_descriptions),
            derived_using="ereignisse",
        )

    if len(current_remain_descriptions) > 0:
        cultural_asset.literal(
            attribute="currentRemainDescription",
            value=", ".join(current_remain_descriptions),
            derived_using="ereignisse",
        )


def create_image(record: etltools.Record) -> etltools.Entity:

    if not record["persistentBildurl"]:
        return None

    image = etltools.Entity(
        identifier=record["laufNr"] + "_image", base_type="Image", derived_from=record
    )
    image.literal(
        attribute="url",
        value=record["persistentBildurl"],
        derived_using="persistentBildurl",
        datatype=XSD.anyURI,
    )

    return image


def relate_classifications_and_materials(
    entity: etltools.Entity, record: etltools.Record, derived_from: str
) -> None:
    input_string = record[derived_from]
    if input_string is None:
        return
    (classification_uris, material_uris) = common.classification_and_material.detect(
        input_string
    )

    for classification_uri in classification_uris:
        entity.related(
            via="classifiedAs",
            with_entity_uri=classification_uri,
            derived_using=derived_from,
        )

    for material_uri in material_uris:
        entity.related(
            via="consistsOfMaterial",
            with_entity_uri=material_uri,
            derived_using=derived_from,
        )


def main():
    output_graph = etltools.create_graph("linz")
    data = etltools.data.csv_as_lines(
        source_id="linz", file_path="scraped_data_with_persistent_img_urls.csv"
    )

    # Create a record for each row in the CSV
    records = []
    for index, line in enumerate(data):
        record = create_record(line, index)
        output_graph += record.to_graph()
        records.append(record)

    # The only collection is "Linzer Sammlung"
    linz_collection = etltools.Entity(
        identifier="Linzer_Sammlung_collection",
        base_type="Collection",
        derived_from=records[0],
    )

    linz_collection.literal(
        attribute="name", value="Linzer Sammlung", derived_using="sammlung"
    )
    output_graph += linz_collection.to_graph()

    # Create a cultural asset for each record
    for record in records:
        cultural_asset = create_cultural_asset(record)
        cultural_asset.related(via="collectedIn", with_entity=linz_collection)
        output_graph += cultural_asset.to_graph()

    etltools.helpers.validate_graph(output_graph)
    etltools.data.write_turtle(output_graph, "linz_output.ttl")

    # to create keyword counts for statistics
    # common.classification_and_material.write_counts("linz")


if __name__ == "__main__":
    main()
