#### This sample etl script demonstrates how to transform a CSV file into a graph using the ETL tools provided by the ETL library.
#### The script is not executable and serves as a reference for how to use the ETL tools.

from etl import etltools, common

graph = etltools.create_graph("my_source_identifier")

# CSV lines -> Records (and add them to the graph)
# it is important that your data is in the folder data/my_sourcs_identifier/my_data_file.csv
lines = etltools.data.csv_as_lines(source_id="my_source_identifier", file_path="my_data_file", limit=10)

# add records to the graph
records = []
for index, line in enumerate(lines):
    record = etltools.Record(
        source_id="my_source_identifier", collection_id="card", record_id=str(index), data=line
    )
    graph += record.to_graph()
    records.append(record)

# Records -> Entities (and add them to the graph)
for record in records:
    # For each record, create a CulturalAsset entity
    cultural_asset = etltools.Entity(
        identifier=record["unique_identifier"], base_type="CulturalAsset", derived_from=record
    )

    # Trivial case: Directly copy over the "objectTitle" column from the CSV into the "title" schema attribute
    # The attribute value has to be definied in the ontology and the derived_using has to be the column name in the dataset
    cultural_asset.literal(attribute="title", derived_using="objectTitle")

    # Rule-based data preperation: taxonomy mapping
    (classification_uris1, material_uris1) = common.classification_and_material.detect(
        record["material"]
    )
    (classification_uris2, material_uris2) = common.classification_and_material.detect(
        record["classification"]
    )
    classification_uris = classification_uris1 + classification_uris2
    material_uris = material_uris1 + material_uris2

    for classification_uri in classification_uris:
        cultural_asset.related(
            via="classifiedAs",
            with_entity_uri=classification_uri,
            derived_using="material",
        )
    for material_uri in material_uris:
        cultural_asset.related(
            via="consistsOfMaterial",
            with_entity_uri=material_uri,
            derived_using="material",
        )


    # Entity creation: If the artist column is not empty, create a Person entity based on the "artist" column in the CSV
    if record["artist"] is not None:
        creator = etltools.Entity(
            identifier=record["cardId"] + "_creator",
            base_type="Person",
            derived_from=record,
        )
        creator.literal(attribute="name", derived_using="artist")
        cultural_asset.related(via="creator", with_entity=creator)

    graph += cultural_asset.to_graph()

etltools.data.write_turtle(graph, "my_source_identifier_output.ttl")
