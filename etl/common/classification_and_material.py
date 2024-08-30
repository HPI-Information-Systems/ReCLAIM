import json
import re
import os
import Levenshtein
from etl import etltools

rules = [
    {
        "keywords": ["bust", "büste"],
        "classifications": ["bust"],
        "materials": [],
    },
    {
        "keywords": ["altar"],
        "classifications": ["religiousObject"],
        "materials": [],
    },
    {
        "keywords": ["vase", "rahmen", "krug", "teller"],
        "classifications": ["decorativeArts"],
        "materials": [],
    },
    {
        "keywords": ["leather", "leatherwork", "leder"],
        "classifications": ["leatherwork"],
        "materials": [],
    },
    {
        "keywords": [
            "metalwork",
            "metalworks",
            "metalwonkures",
            "metalworksures",
            "chetalwork",
            "löffel",
        ],
        "classifications": ["metalwork"],
        "materials": [],
    },
    {"keywords": ["textiles"], "classifications": ["textile"], "materials": []},
    {
        "keywords": ["ceramics", "keramiken"],
        "classifications": ["ceramics"],
        "materials": [],
    },
    {
        "keywords": ["sculptures", "sculpture", "skulptur", "statuette"],
        "classifications": ["sculpture"],
        "materials": [],
    },
    {
        "keywords": ["woodwork", "holzschnitte"],
        "classifications": ["woodwork"],
        "materials": ["wood"],
    },
    {
        "keywords": ["numismatic collection", "numismatics"],
        "classifications": ["numismaticCollection"],
        "materials": [],
    },
    {"keywords": ["lighting"], "classifications": ["lightingDevice"], "materials": []},
    {"keywords": ["book", "buch"], "classifications": ["book"], "materials": []},
    {
        "keywords": ["manuscript", "incunabula", "manuscripts"],
        "classifications": ["manuscript"],
        "materials": [],
    },
    {
        "keywords": ["painting", "gemälde", "bild", "halbfigur"],
        "classifications": ["painting"],
        "materials": [],
    },
    {
        "keywords": ["picture", "photograph", "photogr.", "photo", "foto", "bild"],
        "classifications": ["picture"],
        "materials": [],
    },
    {
        "keywords": ["tapestry", "gobelin", "teppich"],
        "classifications": ["tapestry"],
        "materials": [],
    },
    {
        "keywords": ["furniture", "möbel", "tisch", "schrank", "kommode", "hocker"],
        "classifications": ["furniture"],
        "materials": [],
    },
    {
        "keywords": ["drawing", "zeichnung"],
        "classifications": ["drawing"],
        "materials": [],
    },
    {
        "keywords": ["pencil", "bleistift"],
        "classifications": ["pencilDrawing"],
        "materials": [],
    },
    {
        "keywords": ["etching", "radierung"],
        "classifications": ["etchingPrint"],
        "materials": [],
    },
    {
        "keywords": ["lithographie", "lithography", "lithografie"],
        "classifications": ["lithography"],
        "materials": [],
    },
    {
        "keywords": ["scientific collection", "scientific"],
        "classifications": ["scientificCollection"],
        "materials": [],
    },
    {"keywords": ["archives"], "classifications": ["archive"], "materials": []},
    {
        "keywords": ["military", "trophies", "militär"],
        "classifications": ["militaryTrophies"],
        "materials": [],
    },
    {
        "keywords": ["engraving", "engravings", "kupferstich", "stich"],
        "classifications": ["engravingPrint"],
        "materials": [],
    },
    {
        "keywords": ["print", "prints", "druck", "schabkunstblatt"],
        "classifications": ["print"],
        "materials": [],
    },
    {
        "keywords": ["tapestry", "tapestries", "tapisserie"],
        "classifications": ["tapestry"],
        "materials": [],
    },
    {"keywords": ["judaica", "torah"], "classifications": ["judaica"], "materials": []},
    {
        "keywords": ["glass", "glas"],
        "classifications": ["glass"],
        "materials": ["glass"],
    },
    {
        "keywords": ["jewelry", "jewelery", "schmuck", "amulett"],
        "classifications": ["jewelry"],
        "materials": [],
    },
    {
        "keywords": ["wood and brass"],
        "classifications": [],
        "materials": ["wood", "brass"],
    },
    {
        "keywords": ["enamel on copper"],
        "classifications": [],
        "materials": ["enamel", "copper"],
    },
    {"keywords": ["paper", "papier"], "classifications": [], "materials": ["paper"]},
    {"keywords": ["limestone"], "classifications": [], "materials": ["limestone"]},
    {"keywords": ["china"], "classifications": [], "materials": ["ceramic"]},
    {
        "keywords": ["cardboard", "presspappe"],
        "classifications": [],
        "materials": ["cardboard"],
    },
    {"keywords": ["leather", "leder"], "classifications": [], "materials": ["leather"]},
    {
        "keywords": ["canvas", "leinwand", "lwd"],
        "classifications": [],
        "materials": ["canvas"],
    },
    {"keywords": ["enamel"], "classifications": [], "materials": ["enamel"]},
    {"keywords": ["terracotta"], "classifications": [], "materials": ["terracotta"]},
    {
        "keywords": ["ivory", "ivories", "elfenbein"],
        "classifications": [],
        "materials": ["ivory"],
    },
    {
        "keywords": [
            "watercolor",
            "water colour",
            "water color",
            "watercolour",
            "waterco",
            "aquarell",
            "gouache",
        ],
        "classifications": [],
        "materials": ["watercolor"],
    },
    {
        "keywords": ["oil on copper"],
        "classifications": [],
        "materials": ["oilOnCopper"],
    },
    {
        "keywords": ["oil on linen", "oil on canvas", "öl auf leinwand"],
        "classifications": [],
        "materials": ["oilOnCanvas"],
    },
    {"keywords": ["oil on panel"], "classifications": [], "materials": ["oilOnPanel"]},
    {"keywords": ["wool", "wolle"], "classifications": [], "materials": ["wool"]},
    {"keywords": ["silk", "seide"], "classifications": [], "materials": ["silk"]},
    {"keywords": ["panel"], "classifications": [], "materials": ["panel"]},
    {"keywords": ["iron", "eisen"], "classifications": [], "materials": ["iron"]},
    {
        "keywords": ["porcelain", "porzellan", "porc."],
        "classifications": [],
        "materials": ["porcelain"],
    },
    {"keywords": ["steel", "stahl"], "classifications": [], "materials": ["steel"]},
    {"keywords": ["brass", "messing"], "classifications": [], "materials": ["brass"]},
    {"keywords": ["silver", "silber"], "classifications": [], "materials": ["silver"]},
    {
        "keywords": ["copper", "kupfer"],
        "classifications": [],
        "materials": ["copper"],
    },
    {"keywords": ["copper gilt"], "classifications": [], "materials": ["copperGilt"]},
    {
        "keywords": ["silver gilt", "silver partly gilt"],
        "classifications": [],
        "materials": ["silverGilt"],
    },
    {"keywords": ["gold"], "classifications": [], "materials": ["gold"]},
    {
        "keywords": ["precious stones", "amethyst"],
        "classifications": [],
        "materials": ["mineral"],
    },
    {
        "keywords": ["carbon", "kohlenstoff"],
        "classifications": [],
        "materials": ["carbon"],
    },
    {
        "keywords": ["coal", "kohle"],
        "classifications": [],
        "materials": ["coal"],
    },
    {
        "keywords": ["metal", "platinum", "zinc", "lead", "Blei", "metall"],
        "classifications": [],
        "materials": ["metal"],
    },
    {
        "keywords": ["wood and steel"],
        "classifications": [],
        "materials": ["woodAndSteel"],
    },
    {
        "keywords": ["lindenwood", "linden wood", "lind", "linde"],
        "classifications": [],
        "materials": ["lindenwood"],
    },
    {
        "keywords": [
            "wood",
            "walnut",
            "nut",
            "holz",
            "oak",
            "eichenholz",
        ],
        "classifications": [],
        "materials": ["wood"],
    },
    {
        "keywords": [
            "oil on wood",
            "oil on nutwood",
            "oil on oak wood",
            "oil on pinewood",
            "oil on soft wood",
            "oil on plywood",
            "oil on beech wood",
        ],
        "classifications": [],
        "materials": ["oilOnWood"],
    },
    {
        "keywords": ["paint", "painted", "coloured", "col."],
        "classifications": [],
        "materials": ["paint"],
    },
    {"keywords": ["bronze gilt"], "classifications": [], "materials": ["bronzeGilt"]},
    {
        "keywords": ["sandstone", "sandstein"],
        "classifications": [],
        "materials": ["sandstone"],
    },
    {"keywords": ["gilt"], "classifications": [], "materials": ["gilt"]},
    {"keywords": ["marble", "marmor"], "classifications": [], "materials": ["marble"]},
    {
        "keywords": ["oil", "oil on", "öl"],
        "classifications": [],
        "materials": ["oilPaint"],
    },
    {"keywords": ["alabaster"], "classifications": [], "materials": ["alabaster"]},
    {
        "keywords": ["stone", "stoneware", "stein"],
        "classifications": [],
        "materials": ["stone"],
    },
    {
        "keywords": ["limestone", "lime-stone", "lime"],
        "classifications": [],
        "materials": ["limestone"],
    },
    {
        "keywords": ["earthenware", "earthernware", "earthern-ware", "earthen"],
        "classifications": [],
        "materials": ["earthenware"],
    },
    {
        "keywords": ["majolica", "mezzo-maiolica"],
        "classifications": [],
        "materials": ["majolika"],
    },
    {
        "keywords": ["faience", "semi-faience", "fayence"],
        "classifications": [],
        "materials": ["faience"],
    },
    {"keywords": ["bronze"], "classifications": [], "materials": ["bronze"]},
    {
        "keywords": ["plaster", "gips", "gypsum"],
        "classifications": [],
        "materials": ["plaster"],
    },
    {"keywords": ["clay", "ton"], "classifications": [], "materials": ["clay"]},
    {"keywords": ["bone"], "classifications": [], "materials": ["bone"]},
    {
        "keywords": ["mahogani", "mahogany", "mahagoniholz"],
        "classifications": [],
        "materials": ["mahogany"],
    },
    {"keywords": ["stucco"], "classifications": [], "materials": ["stucco"]},
    {"keywords": ["pottery"], "classifications": [], "materials": ["pottery"]},
    {
        "keywords": ["cotton", "velvet", "baumwolle", "cloth"],
        "classifications": [],
        "materials": ["clothingMaterial"],
    },
    {
        "keywords": ["stoff"],
        "classifications": [],
        "materials": ["wovenCloth"],
    },
    {
        "keywords": ["instruments", "instrument"],
        "classifications": ["musicalInstrument"],
        "materials": [],
    },
    {
        "keywords": ["schibuitchi"],
        "classifications": [],
        "materials": ["copper", "silver"],
    },
    {
        "keywords": ["applied art", "tafel", "kunsthandwerk"],
        "classifications": ["artwork"],
        "materials": [],
    },
    {"keywords": ["tin"], "classifications": [], "materials": ["tin"]},
    {
        "keywords": ["rhinoceros-horn"],
        "classifications": [],
        "materials": ["skeletonPart"],
    },
    {
        "keywords": ["nicht vorhanden", "various", "ohne angaben", "unleserlich", "K.A.", "K. A,"],
        "classifications": [],
        "materials": ["unknown"],
    },
    {
        "keywords": ["pastell", "pastel"],
        "classifications": [],
        "materials": ["pastel"],
    },
    {
        "keywords": ["crystal", "kristall", "Bergkristall"],
        "classifications": [],
        "materials": ["crystal"],
    },
    {
        "keywords": ["chalk", "kreide"],
        "classifications": [],
        "materials": ["chalk"],
    },
    {
        "keywords": ["parchment", "pergament"],
        "classifications": [],
        "materials": ["parchment"],
    },
    {
        "keywords": ["miniature"],
        "classifications": ["miniature"],
        "materials": [],
    },
    {
        "keywords": ["cod. membr."],
        "classifications": ["codex"],
        "materials": ["parchment"],
    },
    {
        "keywords": ["ink", "tinte", "federzeichnung"],
        "classifications": [],
        "materials": ["ink"],
    },
    {
        "keywords": ["pen", "stift"],
        "classifications": [],
        "materials": ["pen"],
    },
    {
        "keywords": ["mother of pearl", "perlmutt"],
        "classifications": [],
        "materials": ["motherOfPearl"],
    },
    {
        "keywords": ["bleistift", "pencil"],
        "classifications": [],
        "materials": ["pencil"],
    },
    {
        "keywords": ["pasteboard", "pappe"],
        "classifications": [],
        "materials": ["pasteboard"],
    },
]


# this method is supposed to handle "['Papier', 'paper']" correctly - this occurs a lot in the munich data
def handle_list(input: str | None) -> str | None:
    if input is None:
        return None

    regex = r"\[\'([^\']+)\'(?:\,\s*\'([^\']+)\')\]"
    match = re.match(regex, input)
    if match is None:
        return [input]

    list = []
    for word in match.groups():
        list.append(word)
    return list


def calculate_thresholds() -> dict:
    thresholds = {}

    for outer_rule in rules:
        for outer_keyword in outer_rule["keywords"]:
            for inner_rule in rules:
                if outer_rule == inner_rule:
                    continue
                for inner_keyword in inner_rule["keywords"]:

                    distance = Levenshtein.distance(outer_keyword, inner_keyword)

                    distance_based_threshold = max(distance - 1, 0)

                    length_based_threshold = 2 if len(outer_keyword) > 3 else 0

                    if outer_keyword not in thresholds:
                        thresholds[outer_keyword] = min(
                            distance_based_threshold, length_based_threshold
                        )
                    else:
                        thresholds[outer_keyword] = min(
                            distance_based_threshold,
                            length_based_threshold,
                            thresholds[outer_keyword],
                        )

    return thresholds


thresholds = calculate_thresholds()

counts = {}


def detect(value: str) -> (list[str], list[str]):
    '''This method detects the classification and material of an object based on the given value. 
    
    The method matches the input value with the keywords in the rules.
    It returns a tuple of two lists, the first one containing the classifications and the second one containing the materials. '''
    global counts
    global thresholds
    
    # Remove all non-ASCII characters
    value = re.sub(r"[^\x00-\x7F]", "", value)

    # Normalize to lowercase
    value = value.lower()

    # Split the string by spaces and slashes
    substrings = re.split(r"\s+|/", value)
    # If there is only one substring added so far, it is not neccessary to add the entire string as well, as it would be the same
    if len(substrings) > 1:
        substrings.append(value)

    classifications = set()
    materials = set()

    for substring in substrings:
        for rule in rules:
            for keyword in rule["keywords"]:
                distance = Levenshtein.distance(keyword, substring)

                if (
                    distance <= thresholds[keyword]
                    or substring.startswith(keyword)
                    or substring.endswith(keyword)
                ):
                    for classification in rule["classifications"]:
                        classification_uri = etltools.uris.taxonomies(
                            "classification", classification
                        )
                        classifications.add(classification_uri)

                    for material in rule["materials"]:
                        material_uri = etltools.uris.taxonomies("material", material)
                        materials.add(material_uri)

                    if keyword not in counts:
                        counts[keyword] = 1
                    else:
                        counts[keyword] += 1

    return (list(classifications), list(materials))


def detect_list(value: str) -> (list[str], list[str]):
    '''This method handels an input that is a list and than calls the detect method for each value in the list.'''
    values = handle_list(value)
    all_classifications = set()
    all_materials = set()
    for value in values:
        classifications, materials = detect(value)
        all_classifications.update(classifications)
        all_materials.update(materials)

    return (list(all_classifications), list(all_materials))


def write_counts(source: str):
    '''This method writes the counts of the detected keywords to a file in the analytics folder.'''
    global counts
    folder = "../analytics"
    filename = f"material_classification_match_counts_{source}.txt"
    path = os.path.join(folder, filename)

    sorted_counts = dict(sorted(counts.items(), key=lambda item: item[0]))
    sum = 0

    with open(path, "w") as f:
        for key, value in sorted_counts.items():
            f.write(f"{key}: {value}\n")
            sum += value

        f.write(f"\nTotal: {sum}\n")

    counts = {}
