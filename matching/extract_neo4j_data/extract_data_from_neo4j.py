import enum
import json
from neo4j import Session, GraphDatabase

from config import get_settings

settings = get_settings()

DRIVER = GraphDatabase.driver(
    uri=settings.NEO4J_URI, auth=(settings.NEO4J_USERNAME, settings.NEO4J_PASSWORD)
)

class SupportedSource(enum.Enum):
    """
    Enum for the different sources.
    """

    ERR = "err"  # Einsatzstab Reichsleiter Rosenberg
    WCCP = "wccp"  # Wiesbaden Central Collection Point
    LINZ = "linz"  # Sonderauftrag Linz
    MCCP = "munich"  # Munich Central Collection Point
    MACCP = "marburg"  # Marburg Central Collection Point
    GOER = "goer"  # Hermann Göring Collection

def rm_newlines_tabs(str):
    return str.replace("\n", " ").replace("\t", " ").strip().replace("  ", " ")

def extract_person_attributes(person_data) -> str:
    person_name = []

    if "jdcrp__name" in person_data:
        person_name.append(person_data["jdcrp__name"])
    if "jdcrp__firstName" in person_data:
        person_name.append(person_data["jdcrp__firstName"])
    if "jdcrp__lastName" in person_data:
        person_name.append(person_data["jdcrp__lastName"])
    if "jdcrp__pseudonym" in person_data:
        person_name.append(person_data["jdcrp__pseudonym"])
    if "jdcrp__birthDate" in person_data:
        person_name.append(person_data["jdcrp__birthDate"])
    if "jdcrp__deathDate" in person_data:
        person_name.append(person_data["jdcrp__deathDate"])
    if "jdcrp__lifetime" in person_data:
        person_name.append(person_data["jdcrp__lifetime"])
    
    return rm_newlines_tabs(" ".join(person_name))


def remove_escape_sequences(text: str) -> str:
    return text.replace("\r\n", " ").replace("\n", " ").replace("\r", " ").replace("\t", " ").strip()


def clean_response_entity_dict(entity_dict: dict, entity_type: str) -> dict:
    if entity_dict is None:
        return {}
    entity_dict.pop("jdcrp__derivedUsingMapping", None)
    return {
        key.replace("jdcrp_", entity_type).replace("uri", entity_type + "_uri"): remove_escape_sequences(value)
        for key, value in entity_dict.items()
        if value is not None
    }


def get_matching_candidate_pairs(session: Session = DRIVER.session()):

    db_response = session.run(
        """
        MATCH (assetA:jdcrp__CulturalAsset), (assetB:jdcrp__CulturalAsset)
        WITH *, apoc.text.split(assetA.uri, '/')[4] AS sourceA, apoc.text.split(assetB.uri, '/')[4] AS sourceB
        WHERE NOT sourceA = sourceB AND assetA.jdcrp__title < assetB.jdcrp__title
        WITH *, 
            apoc.text.split(assetA.jdcrp__title, ' ') AS wordsN, 
            apoc.text.split(assetB.jdcrp__title, ' ') AS wordsM
        WHERE size(wordsN) >= 5 AND size(wordsM) >= 5
        WITH assetA, assetB, [word IN wordsN WHERE word IN wordsM AND size(word) >= 4] AS sharedWords 
        WHERE size(sharedWords) >= 3
        OPTIONAL MATCH (assetA)-[:jdcrp__createdBy]->(assetA_creator:jdcrp__Person)
        OPTIONAL MATCH (assetB)-[:jdcrp__createdBy]->(assetB_creator:jdcrp__Person)
        RETURN assetA, assetB, assetA_creator, assetB_creator, sharedWords
        """
    ).data()

    jsonl_output: str = ""
    match_pair: list[dict] = []

    for record in db_response:

        match_pair.append(
            clean_response_entity_dict(record["assetA"], "CulturalAsset")
            | clean_response_entity_dict(record["assetA_creator"], "Person")
        )
        match_pair.append(
            clean_response_entity_dict(record["assetB"], "CulturalAsset")
            | clean_response_entity_dict(record["assetB_creator"], "Person")
        )
        jsonl_output += json.dumps(match_pair, ensure_ascii=False) + "\n"
        match_pair.clear()

    with open("matching_cadidates_common_title.jsonl", "w", encoding="utf-8") as f:
        f.write(jsonl_output)


def get_all_assets_with_creators(session: Session = DRIVER.session()):

    db_response = session.run(
        """
        MATCH (asset:jdcrp__CulturalAsset)
        OPTIONAL MATCH (asset)-[:jdcrp__createdBy]->(creator:jdcrp__Person)
        RETURN asset, creator
        """
    ).data()

    entities: list[dict] = []

    for record in db_response:
        asset_dict = clean_response_entity_dict(record["asset"], "CulturalAsset")
        asset_dict["creator"] = clean_response_entity_dict(record["creator"], "Person")
        entities.append(asset_dict)

    with open("all_assets.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(entities, ensure_ascii=False, indent=4))


def get_all_persons_with_uris(session: Session = DRIVER.session()):

    db_response = session.run(
        """
        MATCH (p:jdcrp__Person)
        RETURN properties(p) AS person
        """
    ).data()

    entities: list[str] = []

    for record in db_response:
        person = record["person"]
        person_name = extract_person_attributes(person)
        if len(person_name) > 0:
            entities.append(person_name + "\t" + person["uri"] + "\n")

    with open("all_persons.csv", "w", encoding="utf-8") as f:
        f.writelines(entities)


def get_all_titles_with_uris(session: Session = DRIVER.session()):

    db_response = session.run(
        """
        MATCH (c:jdcrp__CulturalAsset)
        WHERE size(c.jdcrp__title) > 1
        RETURN c.jdcrp__title AS title, c.uri AS uri
        """
    ).data()

    entities: list[str] = ["value\turi\n"]

    for record in db_response:
        title = rm_newlines_tabs(record["title"])
        uri = record["uri"]
        entities.append(title + "\t" + uri + "\n")

    with open("all_asset_titles.csv", "w", encoding="utf-8") as f:
        f.writelines(entities)


def get_descriptions(session: Session = DRIVER.session()):
    source = SupportedSource.ERR

    db_response = session.run(
        """
            MATCH (cultural_asset:jdcrp__CulturalAsset)
            WHERE cultural_asset.uri STARTS WITH $uri_source_prefix
            RETURN cultural_asset.jdcrp__physicalDescription AS title
        """,
        uri_source_prefix="https://graph.jdcrp.org/sources/" + source.value,
    ).data()

    titles = set()

    with open(f"descriptions_{source.value}.txt", "w", encoding="utf-8") as f:
        for record in db_response:
            title = record["title"]
            if title:
                title = title.splitlines()[0]
                title = (
                    title.replace("\n", " ")
                    .replace("\r", "")
                    .replace("\t", " ")
                    .strip()
                )
                if len(title) >= 15 and title.lower() not in titles:
                    titles.add(title.lower())
                    f.write(title + "\n")

def get_titles(session: Session = DRIVER.session()):
    source = SupportedSource.ERR

    db_response = session.run(
        """
            MATCH (cultural_asset:jdcrp__CulturalAsset)
            WHERE cultural_asset.uri STARTS WITH $uri_source_prefix
            RETURN cultural_asset.jdcrp__title AS title
        """,
        uri_source_prefix="https://graph.jdcrp.org/sources/" + source.value,
    ).data()

    titles = set()

    with open(f"titles_{source.value}.txt", "w", encoding="utf-8") as f:
        for record in db_response:
            title = record["title"]
            if title:
                title = (
                    title.replace("\n", " ")
                    .replace("\r", "")
                    .replace("\t", " ")
                    .strip()
                )
                if len(title) >= 5 and title.lower() not in titles:
                    titles.add(title.lower())
                    f.write(title + "\n")



def get_similar_entity_edge_pairs(session: Session = DRIVER.session()):

    db_response = session.run(
        """
        MATCH (assetA:jdcrp__CulturalAsset)-[:jdcrp__similarEntity]->(assetB:jdcrp__CulturalAsset)
        WHERE assetB.uri CONTAINS "/linz/"
        OPTIONAL MATCH (assetA)-[:jdcrp__createdBy]->(assetA_creator:jdcrp__Person)
        OPTIONAL MATCH (assetB)-[:jdcrp__createdBy]->(assetB_creator:jdcrp__Person)
        RETURN assetA, assetB, assetA_creator, assetB_creator
        """
    ).data()

    jsonl_output: str = ""
    match_pair: list[dict] = []

    for record in db_response:

        match_pair.append(
            clean_response_entity_dict(record["assetA"], "CulturalAsset")
            | clean_response_entity_dict(record["assetA_creator"], "Person")
        )
        match_pair.append(
            clean_response_entity_dict(record["assetB"], "CulturalAsset")
            | clean_response_entity_dict(record["assetB_creator"], "Person")
        )
        jsonl_output += json.dumps(match_pair, ensure_ascii=False) + "\n"
        match_pair.clear()

    with open("err_linz_goldstandard.jsonl", "w", encoding="utf-8") as f:
        f.write(jsonl_output)
         


if __name__ == "__main__":
    get_all_titles_with_uris()
    DRIVER.close()