from etl import etltools


def get_classification_uri(artTypeId):
    '''this function returns the classification uri for the given artTypeId'''
    artType_classification_mapping = {
        "4": "ceramics",
        "17": "metalwork",
        "53": "unknown",
        "74": "engravingPrint",
        "115": "unknown",
        "246": "painting",
        "247": "worksOnPaper",
        "248": "sculpture",
        "249": "decorativeArts",
        "250": "antiquities",
        "265": "writtenWork",
        "266": "judaica",
        "267": "musicalInstrument",
    }
    name = artType_classification_mapping[artTypeId]

    return etltools.uris.taxonomies("classification", name)


# 4, 17, 74, 115 occur only one in the artypeId column but are not defined in the arttype table
# as each of them occur only once, they were matched to classifications manually
