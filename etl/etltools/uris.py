def jdcrp(path: str):
    return "https://graph.jdcrp.org/" + path


def schema(attribute_name: str) -> str:
    return jdcrp("schema#" + attribute_name)


def raw(source_id: str, path: str):
    return jdcrp("raw/" + source_id + "#" + path)


def entity(source_id: str, base_entity_type: str, identifier: str):
    return jdcrp("sources/" + source_id + "/" + base_entity_type + "#" + identifier)


def taxonomies(taxonomy_name: str, identifier: str):
    return jdcrp("taxonomies/" + taxonomy_name + "#" + identifier)
