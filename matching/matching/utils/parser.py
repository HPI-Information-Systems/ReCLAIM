"""
Parsing utilities for the neo4j database
"""


def remove_namespacing(name: str) -> str:
    """
    Remove the namespacing used by neo4j from the name
    """

    if name.startswith("ns") or name.startswith("jdcrp"):
        return "__".join(name.split("__")[1:])
    return name


def parse_uri(uri: str) -> str:
    """
    Parse the uri
    """
    try:
        source = str(uri).split("/")[4]
    except IndexError:
        return uri

    return f"{source}_{str(uri).split("  # ")[-1]}"
