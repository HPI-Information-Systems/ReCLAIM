import os
from typing import Dict
from rdflib import XSD, Namespace
from ontology_parse_properties import (
    get_structured_class_properties_from_ontology,
    ClassProperty,
)

jdcrp = Namespace("https://graph.jdcrp.org/schema#")
xsd = XSD._NS

# Where to write the output schema Python file
schema_file_destination = os.path.join(
    os.path.dirname(__file__), "backend", "schema", "__init__.py"
)

# Defines Taxonomy types.
taxonomy_types = [jdcrp.Material, jdcrp.Classification]

# Defines properties that will not be added to the schema.
ignore_properties = [jdcrp.derivedFrom, jdcrp.derivedUsingMapping]

# Defines entity types that will not be added to the schema.
ignore_entity_types = [jdcrp.Entity]

# Literal properties are defined as entries by default.
# This list defines literal properties that are an exception to this rule, i.e., do not have raw and parsed values.
nonentry_properties = [jdcrp.url, jdcrp.relativeOrder]

# Translation for xsd schema types into Python equivalents
xsd_literal_types_python_mapping = {
    xsd.string: "str",
    xsd.date: "str",
    xsd.dateTime: "str",
    xsd.decimal: "float",
    xsd.integer: "int",
    xsd.anyURI: "str",
}


def camel_to_snake(name: str) -> str:
    """
    Converts a camelCase string to snake_case
    :param name: The camelCase string
    :return: The snake_case string
    """
    return "".join(["_" + i.lower() if i.isupper() else i for i in name]).lstrip("_")


def generate_python_code(properties_dict: Dict[str, Dict[str, ClassProperty]]) -> str:
    """
    Generates the Python Pydantic schema code out of the given dictionary of structured class properties.

    :param properties_dict: Dictionary of class properties
    :return: Generated Python code
    """

    codelines = [
        "#" * 50,
        "### Notice: This schema file is auto-generated from the ontology using the generate_backend_schema.py.",
        "### Do not make changes to this file directly. Instead, modify the ontology and then re-generate this file.",
        "#" * 50,
        "",
        "",
        "from typing import List, Optional",
        "from .base_schema import *",
    ]

    for class_uri, properties in properties_dict.items():
        class_name = class_uri.removeprefix(jdcrp)
        inherits_from = "EntityModel"
        if class_uri in taxonomy_types:
            inherits_from = "TaxonomyModel"
        codelines.append("")
        codelines.append("")
        codelines.append("class " + class_name + "(" + inherits_from + "):")

        for property_name, structured_property in properties.items():
            property_codeline = "    " + camel_to_snake(property_name) + ": "
            num_brackets_opened = 0

            if structured_property.is_optional:
                property_codeline += "Optional["
                num_brackets_opened += 1
            if structured_property.is_list:
                property_codeline += "List["
                num_brackets_opened += 1
            if all(
                [
                    structured_range.is_entry
                    for structured_range in structured_property.property_ranges
                ]
            ):
                property_codeline += "Entry["
                num_brackets_opened += 1

            # Ensure the property ranges are sorted by their name to ensure consistent code generation
            structured_property.property_ranges.sort(key=lambda x: x.range_uri)

            property_python_types = []

            for property_range in structured_property.property_ranges:
                property_name = property_range.range_uri.split("#")[-1]
                if property_range.is_literal:
                    if property_range.range_uri not in xsd_literal_types_python_mapping:
                        print(
                            "Error: Literal type "
                            + property_name
                            + " is not defined in xsd_literal_types_python_mapping. Please add an equivalent Python type and re-run generation."
                        )
                        exit()
                    property_python_types.append(
                        xsd_literal_types_python_mapping[property_range.range_uri]
                    )
                else:
                    property_python_types.append(property_name)

            property_types = " | ".join(property_python_types)

            if structured_property.all_ranges_are_literals():
                property_codeline += property_types
            else:
                property_codeline += '"' + property_types + '"'

            property_codeline += num_brackets_opened * "]"
            if structured_property.is_optional:
                property_codeline += " = None"

            codelines.append(property_codeline)

    codelines.append("")
    return "\n".join(codelines)


if __name__ == "__main__":
    # Write file
    with open(
        schema_file_destination,
        "w",
        encoding="utf-8",
    ) as f:
        f.write(
            generate_python_code(
                get_structured_class_properties_from_ontology(
                    ignore_properties=ignore_properties,
                    ignore_entity_types=ignore_entity_types,
                    nonentry_properties=nonentry_properties,
                )
            )
        )

    print("Successfully wrote the schema file to " + schema_file_destination)
