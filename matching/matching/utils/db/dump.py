import numpy as np
import pandas as pd
from neo4j import GraphDatabase

from matching.utils.parser import remove_namespacing


def dump_database(path: str, uri: str, username: str, password: str) -> pd.DataFrame:
    """Dump the database to a csv-file."""
    driver = GraphDatabase.driver(uri, auth=(username, password))

    page = 0
    limit = 1000

    data = pd.DataFrame()

    with driver.session() as session:
        while True:
            nodes = session.run(
                """
                    MATCH (asset:jdcrp__CulturalAsset)-[r]->(a)
                    WITH asset, r, a,
                        CASE
                            WHEN TYPE(r) = 'jdcrp__consistsOfMaterial' THEN PROPERTIES(a)
                            ELSE NULL
                        END AS materialProperties
                    WITH asset,
                        COLLECT(materialProperties) AS materialProps,
                        COLLECT(CASE WHEN TYPE(r) <> 'jdcrp__consistsOfMaterial' THEN {
                            relationType: TYPE(r),
                            endEntityProperties: PROPERTIES(a)
                        } END) AS otherRelations
                    RETURN {
                        assetProperties: PROPERTIES(asset),
                        materials: [m IN materialProps WHERE m IS NOT NULL],
                        relations: [r IN otherRelations WHERE r IS NOT NULL]
                    } AS cultural_asset
                    SKIP $offset
                    LIMIT $limit;
                """,
                limit=limit,
                offset=page * limit,
            )

            tmp_data = pd.DataFrame()

            if nodes.peek() is None:
                break

            for node in nodes.data():
                node = node["cultural_asset"]
                asset = {**node["assetProperties"]}

                uri = asset["uri"]

                for relation in node["relations"]:
                    relation_name = remove_namespacing(relation["relationType"])
                    counter = 0
                    while relation_name in asset:
                        relation_name = relation_name + "_" + counter

                    for k, v in relation["endEntityProperties"].items():
                        asset[relation_name + "_" + remove_namespacing(k)] = v

                materials = {}

                for relation in node["materials"]:
                    for k, v in relation.items():
                        k = remove_namespacing(k)
                        if k in materials:
                            materials[k].append(v)
                        else:
                            materials[k] = [v]

                for k, v in materials.items():
                    v.sort()
                    relation_name = "consistsOfMaterial"
                    asset[relation_name + "_" + k] = v

                sanitised_asset = {remove_namespacing(k): v for k, v in asset.items()}

                columns = tmp_data.columns
                for k in sanitised_asset.keys():
                    if k not in columns:
                        tmp_data[k] = None

                if len(tmp_data.columns) != len(columns):
                    tmp_data = tmp_data.copy()

                tmp_data.loc[uri] = {
                    k: v if k in sanitised_asset else None
                    for k, v in sanitised_asset.items()
                }

            page += 1

            data = pd.concat([data, tmp_data])

    if path is not None:
        data.to_csv(path, index=True)

    return data
