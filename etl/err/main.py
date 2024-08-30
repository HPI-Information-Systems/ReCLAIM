import os.path
import pandas as pd
from typing import List

from rdflib import Graph, XSD

from etl import etltools
from err import preparation


authors_cache_path = os.path.join(
    os.path.dirname(__file__), "../parse_authors_column_cache.json"
)
authors_cache = etltools.JsonCache(authors_cache_path)


def create_records_with_additional_attributes(
    graph: Graph,
    collection_id: str,
    file_path: str,
    identifier_key: str,
    additional_attribute_object_type: int,
) -> List[etltools.Record]:
    lines = etltools.data.csv_as_lines(source_id="err", file_path=file_path)
    additional_attributes_by_card_id = get_additional_attributes(
        additional_attribute_object_type
    )

    records = []
    for index, line in enumerate(lines):
        identifier = line[identifier_key]

        record = etltools.Record(
            source_id="err",
            collection_id=collection_id,
            record_id=identifier,
            data=line | additional_attributes_by_card_id.get(identifier, {}),
        )

        graph += record.to_graph()
        records.append(record)

    return records


def create_records(
    graph: Graph, collection_id: str, file_path: str
) -> List[etltools.Record]:
    lines = etltools.data.csv_as_lines(source_id="err", file_path=file_path)
    records = []
    for index, line in enumerate(lines):
        record = etltools.Record(
            source_id="err",
            collection_id=collection_id,
            record_id=str(index),
            data=line,
        )
        graph += record.to_graph()
        records.append(record)

    return records


def get_additional_attributes(object_type: int) -> dict[str, dict[str, str]]:
    attributes_df = etltools.data.csv_as_dataframe(
        source_id="err", file_path="Attribute.csv"
    )
    values_df = etltools.data.csv_as_dataframe(
        source_id="err", file_path="AttributeValue.csv"
    )

    # Filter by object type: 1 = Collection, 2 = Card, 4 = Owner
    attributes_df.query('ObjectType == "' + str(object_type) + '"', inplace=True)

    joined_df = values_df.merge(attributes_df, on="AttributeId")

    # Create a dictionary of lists of attributes, keyed by card_id
    attributes_by_card_id = {}

    for _, row in joined_df.iterrows():
        card_id = row["ObjectId"]
        attribute_name = "additional_attribute_" + row["Attribute"]
        attribute_value = row["AttributeValue"]

        if card_id not in attributes_by_card_id:
            attributes_by_card_id[card_id] = {}

        attributes_by_card_id[card_id][attribute_name] = attribute_value

    return attributes_by_card_id


def aggregate_grouped_getty_artists(group: pd.DataFrame) -> pd.Series:
    return pd.Series(
        {
            "name": group["TERM"].iloc[0],
            # use the longest biography
            "biography": group["biography"].max(),
            # use the most common birth_date and death_date
            "birth_date": group["birth_date"].mode().iloc[0]
            if len(group["birth_date"].mode()) > 0
            else None,
            "death_date": group["death_date"].mode().iloc[0]
            if len(group["death_date"].mode()) > 0
            else None,
        }
    )


def get_getty_artists() -> pd.DataFrame:
    getty_artists = etltools.data.csv_as_dataframe(
        source_id="err", file_path="ERR_ArtistName1.csv"
    )

    # iterate over getty_artists grouped by TERM
    df = (
        getty_artists.groupby("TERM", sort=False)
        .apply(aggregate_grouped_getty_artists)
        .reset_index(drop=True)
    )

    return df


def create_cultural_asset_entities(
    graph: Graph, cultural_asset_records: List[etltools.Record]
):
    getty_artists = get_getty_artists()

    for idx, record in enumerate(cultural_asset_records):

        if idx % 500 == 0 or idx == len(cultural_asset_records) - 1:
            print(
                f"Created {idx+1} / {len(cultural_asset_records)} cultural asset entities.."
            )

        cultural_asset = etltools.Entity(
            identifier=record["cardId"], base_type="CulturalAsset", derived_from=record
        )

        if record["collectionId"] is not None:
            cultural_asset.related(
                via="collectedIn",
                with_entity_uri=etltools.uris.entity(
                    source_id="err",
                    base_entity_type="Collection",
                    identifier=record["collectionId"],
                ),
            )

        # if record["ownerId"] is not None:
        #     confiscation = etltools.Entity(
        #         identifier=record["cardId"] + "_confiscation",
        #         base_type="ConfiscationEvent",
        #         derived_from=record,
        #     )
        #     confiscation.related(
        #         via="confiscatedFromLegalEntity",
        #         with_entity_uri=etltools.uris.entity(
        #             source_id="err",
        #             base_entity_type="Person",
        #             identifier=record["ownerId"],
        #         ),
        #     )
        #     cultural_asset.related(
        #         via="affectedCulturalAsset", with_entity=confiscation, inverse=True
        #     )

        if record["artTypeId"] is not None:
            classification_uri = preparation.art_type.get_classification_uri(
                record["artTypeId"]
            )
            etltools.Entity.related(
                cultural_asset,
                via="classifiedAs",
                with_entity_uri=classification_uri,
                derived_using="artTypeId",
            )

        potential_getty_artist = None
        if record["gettyArtist"] is not None:
            matching_artists = getty_artists[
                getty_artists["name"] == record["gettyArtist"]
            ]
            if matching_artists.empty:
                print(f"Getty artist not found for cardId {record['cardId']}")
            else:
                matching_artists = matching_artists.iloc[0]

        if (getty_artist := potential_getty_artist) is not None:
            creator = etltools.Entity(
                identifier=record["cardId"] + "_creator",
                base_type="Person",
                derived_from=record,
            )

            creator.literal(
                attribute="name",
                value=getty_artist["name"],
                derived_using="gettyArtist",
            )

            if getty_artist["biography"] is not None:
                cultural_asset.literal(
                    attribute="historyDescription",
                    value=getty_artist["biography"],
                    derived_using="gettyArtist",
                )
            if getty_artist["birth_date"] is not None:
                creator.literal(
                    attribute="birthDate",
                    value=getty_artist["birth_date"],
                    derived_using="gettyArtist",
                )
            if getty_artist["death_date"] is not None:
                creator.literal(
                    attribute="deathDate",
                    value=getty_artist["death_date"],
                    derived_using="gettyArtist",
                )

            graph += creator.to_graph()
            cultural_asset.related(via="createdBy", with_entity=creator)
        elif record["artist"] is not None:
            creator = etltools.Entity(
                identifier=record["cardId"] + "_creator",
                base_type="Person",
                derived_from=record,
            )

            if authors_cache.has(record["artist"]):
                parsed_author = authors_cache.get(record["artist"])
                if parsed_author["name"] is not None:
                    creator.literal(
                        attribute="name",
                        value=parsed_author["name"],
                        derived_using="artist",
                    )
                if parsed_author["pseudonym"] is not None:
                    creator.literal(
                        attribute="pseudonym",
                        value=parsed_author["pseudonym"],
                        derived_using="artist",
                    )
                if parsed_author["styleOfStr"] is not None:
                    cultural_asset.literal(
                        attribute="annotation",
                        value=parsed_author["styleOfStr"],
                        derived_using="artist",
                    )
                if parsed_author["dateStr"] is not None:
                    creator.literal(
                        attribute="lifetime",
                        value=parsed_author["dateStr"],
                        derived_using="artist",
                    )
                    cultural_asset.literal(
                        attribute="creationDate",
                        value=parsed_author["dateStr"],
                        derived_using="artist",
                    )
                if parsed_author["locationStr"] is not None:
                    location = etltools.Entity(
                        identifier=record["cardId"] + "_creation_location",
                        base_type="Location",
                        derived_from=record,
                    )
                    location.literal(
                        attribute="description",
                        value=parsed_author["locationStr"],
                        derived_using="artist",
                    )
                    graph += location.to_graph()
                    cultural_asset.related(
                        via="createdInLocation", with_entity=location
                    )
            else:
                creator.literal(attribute="name", derived_using="artist")

            graph += creator.to_graph()
            cultural_asset.related(via="createdBy", with_entity=creator)

        if record["artist"] is not None and record["gettyArtist"] is not None:
            print(f"Both artist and gettyArtist are set for cardId {record['cardId']}")

        # if record["objectDestinationByERR"] is not None:
        #     collection_uri = preparation.destination.get_collection_uri(
        #         record["objectDestinationByERR"]
        #     )
        #     location_uri = preparation.destination.get_location_uri(
        #         record["objectDestinationByERR"]
        #     )

        #     transfer_event = etltools.Entity(
        #         identifier=record["cardId"] + "_destination_transfer",
        #         base_type="TransferEvent",
        #         derived_from=record,
        #     )

        #     if collection_uri is not None:
        #         transfer_event.related(
        #             via="toCollection",
        #             with_entity_uri=collection_uri,
        #             derived_using="objectDestinationByERR",
        #         )

        #     if location_uri is not None:
        #         transfer_event.related(
        #             via="toLocation",
        #             with_entity_uri=location_uri,
        #             derived_using="objectDestinationByERR",
        #         )

        #     cultural_asset.related(
        #         via="affectedCulturalAsset", with_entity=transfer_event, inverse=True
        #     )

        cultural_asset.literal(attribute="title", derived_using="objectTitle")
        cultural_asset.literal(
            attribute="physicalDescription", derived_using="objectDesc"
        )
        cultural_asset.literal(
            attribute="archivalSourceDescription", derived_using="objectArchivalSource"
        )
        cultural_asset.literal(
            attribute="bibliography", derived_using="objectBibliography"
        )
        # TODO We don't have the gettyArtist field in the backend schema yet.
        # cultural_asset.literal(
        #    attribute="gettyArtist", derived_using="gettyArtist"
        # )  # TODO: Add this to source related source person.
        cultural_asset.literal(
            attribute="errNumber", derived_using="errId"
        )  # TODO: Wait for data used on website and then use transfer events.
        if record["objectPostConfiscationHistory"] is not None:
            cultural_asset.literal(
                attribute="postConfiscationHistoryDescription",
                value=preparation.html_links.remove(
                    record["objectPostConfiscationHistory"]
                ),
                derived_using="objectPostConfiscationHistory",
            )  # TODO: Decode history in events using LLM. See rules for data cleaning and building multiple entites from one csv field.

        cultural_asset.literal(
            attribute="munichNumber",
            derived_using="additionalAttributeMunichNo",
        )

        cultural_asset.literal(
            attribute="linzNumber",
            derived_using="additionalAttributeLinzNo",
        )

        graph += cultural_asset.to_graph()


def create_collection_entities(graph: Graph, collection_records: List[etltools.Record]):
    for idx, record in enumerate(collection_records):

        if idx % 500 == 0 or idx == len(collection_records) - 1:
            print(f"Created {idx+1} / {len(collection_records)} collection entities..")

        collection = etltools.Entity(
            identifier=record["collectionId"],
            base_type="Collection",
            derived_from=record,
        )

        collection.literal(attribute="abbreviation", derived_using="collectionCode")
        collection.literal(attribute="description", derived_using="collectionDesc")

        graph += collection.to_graph()


def create_owner_entities(graph: Graph, owner_records: List[etltools.Record]):
    for idx, record in enumerate(owner_records):

        if idx % 500 == 0 or idx == len(owner_records) - 1:
            print(f"Created {idx+1} / {len(owner_records)} owner entities..")

        owner = etltools.Entity(
            identifier=record["ownerId"], base_type="Person", derived_from=record
        )

        # Here is graph used, because we cant get the collection anymore.
        if record["collectionId"] is not None:
            owner.related(
                via="ownedBy",
                with_entity_uri=etltools.uris.entity(
                    source_id="err",
                    base_entity_type="Collection",
                    identifier=record["collectionId"],
                ),
                inverse=True,
            )

        if record["city"] is not None or record["country"] is not None:
            location = etltools.Entity(
                identifier=f"{record['ownerId']}_location",
                base_type="Location",
                derived_from=record,
            )
            location.literal(attribute="city", derived_using="city")
            location.literal(attribute="country", derived_using="country")
            graph += location.to_graph()
            owner.related(via="basedIn", with_entity=location)

        owner.literal(attribute="firstName", derived_using="firstName")
        owner.literal(attribute="lastName", derived_using="lastName")
        owner.literal(
            attribute="archivalSourceDescription", derived_using="archivalSource"
        )
        owner.literal(attribute="historyDescription", derived_using="observations")

        graph += owner.to_graph()


def create_image_entities(
    graph: Graph,
    image_records: List[etltools.Record],
    card_records: List[etltools.Record],
):
    # Ensure that we only create images for cards that actually exist
    card_ids_set = set()
    for record in card_records:
        card_ids_set.add(record["cardId"])

    for idx, record in enumerate(image_records):
        if idx % 500 == 0 or idx == len(image_records) - 1:
            print(f"Created {idx+1} / {len(image_records)} image entities..")

        # There are some images that reference a cardId which is not existant (ex. 101)
        card_id = record["cardId"]
        if card_id not in card_ids_set:
            continue

        image = etltools.Entity(
            identifier=record["imageId"], base_type="Image", derived_from=record
        )
        url = preparation.images.generate_image_url(
            record["imageTypeId"], record["fileNameSmall"]
        )
        image.literal(
            attribute="url",
            value=url,
            derived_using=["fileNameSmall", "imageType"],
            datatype=XSD.anyURI,
        )

        if card_id is not None:
            # if the image is a NARA image, it is a picture of the property card. Otherwise it is a image of the cultural asset.
            if record["imageTypeId"] == "1":
                image.related(
                    via="referencedInCardImage",
                    with_entity_uri=etltools.uris.entity(
                        source_id="err",
                        base_entity_type="CulturalAsset",
                        identifier=record["cardId"],
                    ),
                    inverse=True,
                )
            else:
                image.related(
                    via="depictedInImage",
                    with_entity_uri=etltools.uris.entity(
                        source_id="err",
                        base_entity_type="CulturalAsset",
                        identifier=record["cardId"],
                    ),
                    inverse=True,
                )

        graph += image.to_graph()


def main():
    graph = etltools.create_graph("err")

    print("Started ETL for ERR dataset!")

    print("Creating records for Card.csv")
    card_records = create_records_with_additional_attributes(
        graph=graph,
        collection_id="card",
        file_path="Card.csv",
        identifier_key="CardId",
        additional_attribute_object_type=2,
    )

    print("Creating records for ArtType.csv")
    art_type_records = create_records(
        graph=graph, collection_id="artType", file_path="ArtType.csv"
    )

    print("Creating records for Collection.csv")
    collection_records = create_records_with_additional_attributes(
        graph=graph,
        collection_id="collection",
        file_path="Collection.csv",
        identifier_key="CollectionId",
        additional_attribute_object_type=1,
    )

    print("Creating records for Owner.csv")
    owner_records = create_records_with_additional_attributes(
        graph=graph,
        collection_id="owner",
        file_path="Owner.csv",
        identifier_key="OwnerId",
        additional_attribute_object_type=4,
    )

    print("Creating records for Image.csv")
    image_records = create_records(
        graph=graph, collection_id="image", file_path="Image.csv"
    )

    print("Creating collection entities..")
    create_collection_entities(graph, collection_records)

    print("Creating destination collection and location entities..")
    preparation.destination.add_collection_entities_to_graph(graph)
    preparation.destination.add_location_entities_to_graph(graph)

    print("Creating owne entities..")
    create_owner_entities(graph, owner_records)

    print("Creating cultural asset entities..")
    create_cultural_asset_entities(graph, card_records)

    print("Creating image entities..")
    create_image_entities(graph, image_records, card_records)

    print("Validating output graph...")
    etltools.helpers.validate_graph(graph)

    print("Writing ttl graph to disk..")
    etltools.data.write_turtle(graph, "err_output.ttl")


if __name__ == "__main__":
    main()
