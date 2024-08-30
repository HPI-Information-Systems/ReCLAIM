from urllib.parse import quote
from etl import etltools, common
import re
from munich import preparation

created_classifications = {}
created_materials = {}


# def create_arrival_event(
#     record: etltools.Record, identifier: str
# ) -> etltools.Entity | None:
#     if record["receiptDate"] is None:
#         return None
#     arrival = etltools.Entity(
#         identifier=identifier + "_arrival",
#         base_type="ArrivalEvent",
#         derived_from=record,
#     )
#     arrival.literal(
#         attribute="structuredDate",
#         value=common.dates.german_to_iso(record["receiptDate"]),
#         derived_using="receiptDate",
#         datatype=XSD.dateTime,
#     )
#     return arrival


# def create_departure_event(
#     record: etltools.Record, identifier: str
# ) -> etltools.Entity | None:
#     if record["dispatchDate"] is None:
#         return None
#     departure = etltools.Entity(
#         identifier=identifier + "_departure",
#         base_type="DepartureEvent",
#         derived_from=record,
#     )
#     departure.literal(
#         attribute="structuredDate",
#         value=common.dates.german_to_iso(record["dispatchDate"]),
#         derived_using="dispatchDate",
#         datatype=XSD.dateTime,
#     )
#     return departure


def create_cultural_asset(record: etltools.Record) -> etltools.Entity:
    identifier = quote(record["id"] + "_" + record.get_record_id())

    cultural_asset = etltools.Entity(
        identifier=identifier, base_type="CulturalAsset", derived_from=record
    )
    cultural_asset.literal(attribute="munichNumber", derived_using="id")
    cultural_asset.literal(attribute="title", derived_using="objekt")
    cultural_asset.literal(
        attribute="postConfiscationHistoryDescription",
        derived_using="herkunftVerbleibSozietät",
    )
    cultural_asset.literal(attribute="annotation", derived_using="schlagwort")

    linz1 = record["linzNr(lautDbSonderauftragLinz)"]
    linz2 = record["linzNr(lautKarte)"]

    if (linz1 is not None) and (linz2 is not None):
        if linz1 in linz2:
            cultural_asset.literal(
                attribute="linzNumber",
                value=linz2,
                derived_using=["linzNr(lautDbSonderauftragLinz)", "linzNr(lautKarte)"],
            )
        else:
            cultural_asset.literal(
                attribute="linzNumber",
                value=linz1 + " , " + linz2,
                derived_using=["linzNr(lautDbSonderauftragLinz)", "linzNr(lautKarte)"],
            )
    elif linz1 is not None:
        cultural_asset.literal(
            attribute="linzNumber",
            value=linz1,
            derived_using="linzNr(lautDbSonderauftragLinz",
        )
    elif linz2 is not None:
        cultural_asset.literal(
            attribute="linzNumber", value=linz2, derived_using="linzNr(lautKarte"
        )

    if record["eigentümer"] is not None:
        if not record["eigentümer"].startswith("Bundesarchiv,"):
            raise Exception("Eigentümer does not start with 'Bundesarchiv,'")
        else:
            signatur = record["eigentümer"]
            signatur = re.sub(r"Bundesarchiv, ", "", signatur)
            cultural_asset.literal(
                attribute="bundesarchivSignature",
                value=signatur,
                derived_using="eigentümer",
            )

    measurements = preparation.measurements.merge_measurements(
        record["höhe"], record["breite"], record["länge"]
    )
    cultural_asset.literal(
        attribute="measurements",
        value=measurements,
        derived_using=["höhe", "breite", "länge"],
    )
    relate_classifications_and_materials(cultural_asset, record, "material")
    relate_classifications_and_materials(cultural_asset, record, "objektart")

    cultural_asset.literal(
        attribute="creationDate",
        value=preparation.object_date.parse(record["objectDate"]),
        derived_using="objectDate",
    )

    # arrival = create_arrival_event(record, identifier)
    # cultural_asset.related(
    #     via="affectedCulturalAsset", with_entity=arrival, inverse=True
    # )

    # departure = create_departure_event(record, identifier)
    # cultural_asset.related(
    #     via="affectedCulturalAsset", with_entity=departure, inverse=True
    # )

    return cultural_asset


def relate_classifications_and_materials(
    entity: etltools.Entity, record: etltools.Record, derived_from: str
) -> None:
    input_string = record[derived_from]

    if input_string is None:
        return

    (
        classification_uris,
        material_uris,
    ) = common.classification_and_material.detect_list(input_string)

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


def create_record(row, index):
    return etltools.Record(
        source_id="munich", collection_id="card", record_id=str(index), data=row
    )


def main():
    output_graph = etltools.create_graph("munich")
    # munich_short contains the first 20 columns of munich.csv - if we decide to use more columns we have to change the import here
    data = etltools.data.csv_as_lines(source_id="munich", file_path="munich_short.csv")

    # Create a record for each line in the csv
    records = []
    for index, line in enumerate(data):
        record = create_record(line, index)
        output_graph += record.to_graph()
        records.append(record)

    # Records -> Entities (and add them to the graph)
    for record in records:
        cultural_asset = create_cultural_asset(record)
        output_graph += cultural_asset.to_graph()

    etltools.helpers.validate_graph(output_graph)
    etltools.data.write_turtle(output_graph, "munich_output.ttl")

    # to create keyword counts for statistics
    # common.classification_and_material.write_counts("munich")


if __name__ == "__main__":
    main()
