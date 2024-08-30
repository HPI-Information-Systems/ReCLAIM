from etl import etltools
from rdflib import Graph

destination_code_collections = {
    "57": "goering",
    "72": "goering",
    "80": "goering",
    "81": "goering",
    "83": "goering",
    "84": "fuehrer",
    "85": "goering",
    "114": "goering",
    "115": "goering",
    "116": "fuehrer",
    "117": "ostministerium",
    "119": "ostministerium",
}

collection_names = {
    "goering": "Sammlung Göring",
    "fuehrer": "Sammlung des Führers",
    "ostministerium": "Ostministerium",
}

destination_code_locations = {
    "70": "france",
    "76": "neuschwanstein",
}

location_descriptions = {"france": "Frankreich", "neuschwanstein": "Neuschwanstein"}


def get_collection_uri(destination_code: str) -> str | None:
    if destination_code not in destination_code_collections:
        return None

    collection_id = destination_code_collections[destination_code]
    return etltools.uris.entity("err", "Collection", collection_id)


def get_location_uri(destination_code: str) -> str | None:
    if destination_code not in destination_code_locations:
        return None

    collection_id = destination_code_locations[destination_code]
    return etltools.uris.entity("err", "Location", collection_id)


def add_collection_entities_to_graph(graph: Graph) -> None:
    unique_destination_codes = set(destination_code_collections.values())

    for collection_id in unique_destination_codes:
        # A record is required for each entity (even if the entity is not actually derived from lines of data)
        # For this reason, we create a "dummy" record with the collection name as data and derive the entity from it
        record = etltools.Record(
            source_id="err",
            collection_id="destination_code_collections",
            record_id=collection_id,
            data={"name": collection_names[collection_id]},
        )
        graph += record.to_graph()

        collection = etltools.Entity(
            identifier=collection_id, base_type="Collection", derived_from=record
        )
        collection.literal(attribute="name", derived_using="name")
        graph += collection.to_graph()


def add_location_entities_to_graph(graph: Graph) -> None:
    unique_destination_codes = set(destination_code_locations.values())

    for location_id in unique_destination_codes:
        # A record is required for each entity (even if the entity is not actually derived from lines of data)
        # For this reason, we create a "dummy" record with the collection name as data and derive the entity from it
        record = etltools.Record(
            source_id="err",
            collection_id="destination_code_locations",
            record_id=location_id,
            data={"description": location_descriptions[location_id]},
        )
        graph += record.to_graph()

        location = etltools.Entity(
            identifier=location_id, base_type="Location", derived_from=record
        )
        location.literal(attribute="description", derived_using="description")
        graph += location.to_graph()
