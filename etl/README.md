# Running existing ETL scripts

Make sure you are in the `etl\datasource` directory.

`poetry run python main.py`

The datasources that are currently integrated are:
- err: Einsatzstab Reichsleiter Rosenberg (https://www.errproject.org/jeudepaume/ - provided by JDCRP)
- linz: Sonderauftrag Linz (https://www.dhm.de/datenbank/linzdb/indexe.html)
- margburg: Marburg Central Collection Point (provided by JDCRP)
- munich: Munich Central Collection Point (https://www.dhm.de/datenbank/ccp)
- wiesbaden: Wiesbaden Central Collection Point (provided by JDCRP)
- sample: provides a sample ETL script to understand how to use the etltools and how an ETL script should be structured

# Adding ETL results into the database
The ETL scripts do not automatically add the turtle files into the database.
After your ETL script is ready, you have to execute it to prepare your data.
Then, you need to add the `output.ttl` file to the database.
To add an ETL script to the automatic deployment, add its corresponding main function to the `backend/seed/run_etl_and_seed.py` file.

You can find details on how to do this, in the `backend/README.md`.

# Writing ETL scripts

The following section provides a conceptual overview of how to structure ETL scripts.

**Please note:** Don't implement this yourself. The `etltools` package provides a set of classes and helpers for
creating ETL scripts that conform to these guidelines. Its API is explained in the next chapter
[Using `etltools`](#using-etltools).

## 1) Store raw data as _Records_

For each row of our source data (e.g. CSV line), create a Record instance.

**Example source csv**

| Database ID | Title            | Artist Name       |
|-------------|------------------|-------------------|
| 1           | Mona Lisa        | Leonardo da Vinci |
| 2           | The Starry Night | Vincent van Gogh  |
| 3           | The Night Watch  | Rembrandt         |

**Example records**

```turtle

@prefix raw: <https://graph.jdcrp.org/raw/mySource#> .

raw:record_1
	raw:databaseId "1" ;
	raw:title      "Mona Lisa" ;
	raw:artistName "Leonardo da Vinci" .

raw:record_2
	raw:databaseId "2" ;
	raw:title      "The Starry Night" ;
	raw:artistName "Vincent van Gogh" .

# ...
```

By transforming our raw source data into these triples, we now have a way of referring to the raw rows and values of
the source using URIs.

The main codebase doesn't "know" about any of the record's naming. That's intentional, as the record's attributes are
**meant to be highly source-specific**, effectively matching the source's table columns.

Technically, prefixing and naming the attributes is completely up to the source. However, let's try to stick to these
conventions:

- Even if original column names contain spaces, record attribute names should be beautified to camelCase.
- You may modify the attribute names in other ways to increase readability (e.g. remove parentheses, shorten if very
- long)
- Use the `@prefix raw: &lt;https://graph.jdcrp.org/raw/{sourceIdentifier}/#&gt;` namespace for everything related to
  a source's raw records.
- Use `raw:record_{uniqueId}` for the URIs of individual records.
- Use `raw:{attributeName}` for attribute names.

## 2) Derive source entities

When creating source entities, you may

- apply some data cleaning, parsing
- create other related entities such as locations, persons, events, etc.

**Example source entities**

```turtle
# See 1) Storing raw data as Records
@prefix raw:           <https://graph.jdcrp.org/raw/mySource#> .

# This is our main schema
@prefix jdcrp:         <https://graph.jdcrp.org/schema#> .

# These are the URI namespaces for our entities
@prefix CulturalAsset: <https://graph.jdcrp.org/sources/mySource/CulturalAsset#> .
@prefix Person:        <https://graph.jdcrp.org/sources/mySource/Person#> .
@prefix CreationEvent: <https://graph.jdcrp.org/sources/mySource/CreationEvent#> .

CulturalAsset:1
	a                 jdcrp:CulturalAsset ;
	jdcrp:title       "Mona Lisa" ;
	jdcrp:derivedFrom raw:record_1 ;
	jdcrp::derivedUsingMapping
					  '{"https://graph.jdcrp.org/schema#title": ["https://graph.jdcrp.org/raw/mySource#title"]}' .

Person:A
	a                 jdcrp:Person ;
	jdcrp:firstName   "Leonardo" ;
	jdcrp:lastName    "da Vinci" ;
	jdcrp:derivedFrom raw:record_1 ;
	jdcrp:derivedUsingMapping
					  '{"https://graph.jdcrp.org/schema#firstName": ["https://graph.jdcrp.org/raw/mySource#artistName"], "https://graph.jdcrp.org/schema#lastName": ["https://graph.jdcrp.org/raw/mySource#artistName"]}' .

CreationEvent:X
	a                   jdcrp:CreationEvent ;
	jdcrp:affected      CulturalAsset:1 ;
	jdcrp:involvementOf Person:A .

# ...
```

Using `jdcrp:derivedFrom`, we document which record we derived the existence of this entity from.

In `jdcrp:derivedUsingMapping` we store a JSON string. It must be an object with **URIs of the main ontology as
keys** and **an array of URIs of the raw record's attributes** as keys.
This JSON object allows us to document from which raw attribute(s) each key has been derived.

## 3) Additional structuring of attributes

Some attributes (mostly dates) make sense to be further structured before being queried.

In many cases, this results in a loss of context information, e.g. `January 1st 2000 (early morning)` would be
transformed to the ISO date `2000-01-01`, now lacking the 'early morning' detail.

Hence, we like to keep both versions, for example:

- `jdcrp:intakeDate` as a string and
- `jdcrp:structuredIntakeDate` annotated as a `^^xsd:date`

The attribute prefixed with `structured` can be omitted in cases, in which a structured value cannot be derived from
the original attribute (without the prefix).

# Using `etltools`

Check out `sample/main.py` for a example ETL script. It uses many of the classes and helpers that
are explained below.

All ETL scripts must:

- Add records, corresponding to the raw data
- Add entities, referencing the underlying records

## Working with the output graph

### Create the graph

_Always_ use this helper to create the global "output" graph of your ETL script.
It will set a few namespace bindings and return the graph.

```python
from etl import etltools

graph = etltools.create_graph('my_source_id')
```

### Add subgraphs to the output graph

Add the subgraphs from records and entities to the output graph using `+=`.

```python
from etl import etltools

graph = etltools.create_graph('my_source_id')

# record1, record2 are instances of etltools.Record
graph += record1.to_graph()
graph += record2.to_graph()
```

### Validating the output graph against the schema

It is recommended to validate the output graph against the schema as a final step, before writing it to a file.

```python
etltools.data.validate_graph(graph)  # Throws an exception if invalid
```

The following exception is thrown if the graph is invalid.
Additionally, a validation report is written to `validation_results.txt`.

```
Exception: Graph does not conform to schema. Check validation_results.txt for details
```

### Output the graph as a Turtle file

You _may_ use this helper to serialize the graph in Turtle format. The `output_path` is relative to the current working
directory.

```python
from etl import etltools

graph = etltools.create_graph('err')
# Add records and entities to the graph here
etltools.data.write_turtle(graph, 'my_source_id_output.ttl')
```

## Accessing input data

Input data should be contained in the `data` top level directory. You may use these helpers for accessing the data.

```python
from etl import etltools

# Recommended: Read the /data/my_source_id/Card.csv file as a list of dictionaries
records = etltools.data.csv_as_lines(source_id='my_source_id', file_path='Card.csv')

# Read the /data/my_source_id/Card.csv file as a Pandas Data frame
df = etltools.data.csv_as_dataframe(source_id='my_source_id', file_path='Card.csv')

# Get an absolute path to the data file in /data/my_source_id/Card.csv
path = etltools.data.data_path(source_id='my_source_id', file_path='Card.csv')
```

## Records

### Creating records

```python
from etl import etltools

graph = etltools.create_graph('my_source_id')
lines = etltools.data.csv_as_lines(source_id='my_source_id', file_path='Card.csv')
records = []

for index, line in enumerate(lines):
    record = etltools.Record(
        source_id="my_source_id",
        collection_id="card",
        record_id=str(index),
        data=line
    )
    graph += record.to_graph()
    records.append(record)
```

The following keyword arguments are required:

- `source_id` is the ID of the source, e.g. `err`, `wiesbaden`
- `collection_id` is a unique name for the collection of records, e.g. the database relation it corresponds to. The datasets usually consist of only one CSV, and `card` can be used as the collection_id. It is important to differentiate between the tables only if there are multiple tables in the dataset (e.g., ERR).
- `record_id` is a unique ID for the record, e.g. the primary key of the database relation, the row number in a CSV file
- `data` is a dictionary containing the data of the record

Please note: the keys of the `data` dict will be internally changed to camelCase (e.g. `my_key`, `MyKey` and `My Key`
will all be changed `myKey`). Use the camelCase notation when accessing the data.

### Working with records

```python
# Get the value of the "My Field" column. Note the camelCase notation.
value = record['myField']

# Get the record as a subgraph and add it to the output graph
graph += record.to_graph()

# Get the URI of the record
uri = record.uri()
```

## Entities

### Creating entities

Use the entities class to create entities in the graph.

```python
from etl import etltools

cultural_asset = etltools.Entity(
    identifier=record["cardId"],
    base_type="CulturalAsset",
    derived_from=record
)
```

The following keyword arguments are required:

- `identifier` is a unique identifier for the entity
- `base_type` is the base type of the entity, e.g. `CulturalAsset`, `Person`, `Place` without the `Source` prefix
- `derived_from` is the record that the entity is derived from

```python
from etl import etltools

cultural_asset = etltools.Entity(
    identifier=record["cardId"],
    base_type="CulturalAsset",
    derived_from=record
)
```

### Adding literals to entities

#### Direct mapping

```python
# Shorthand
entity.literal(attribute="title", derived_using="objectTitle")

# Is equivalent to
entity.literal(attribute="title", value=record["objectTitle"], derived_using="objectTitle")
```

#### Mapping to multiple attributes

```python
first_name, last_name = record["artist"].split(" ")

entity.literal(attribute="firstName", value=first_name, derived_using="artist")
entity.literal(attribute="lastName", value=last_name, derived_using="artist")
```

#### Mapping from multiple record columns

```python
result = complex_cleaning_process(record["objectTitle"], record["objectDescription"])

entity.literal(attribute="title", value=result, derived_using=["objectTitle", "objectDescription"])
```

### Literals that are not strings
The default datatype of a literal is a xsd:string.
If you want to add a literal, that has a different datatype, you have to make this explicit.

```python
image.literal(
        attribute="url",
        value=url,
        derived_using=image_key,
        datatype=XSD.anyURI,
    )
```
This is mostly the case for `URIs`and `integer`.

> Note, that backend only handles the following datatypes at the moment:
> xsd.string, xsd.date, xsd.dateTime, xsd.decimal, xsd.integer, xsd.anyURI


### Adding relationships between entities

```python
# Both cultural_asset and person are instances of etltools.Entity
cultural_asset.related(via="creator", with_entity=person)

graph += cultural_asset.to_graph()  # now also contains the person triples
```

If you don't have the entity instance at hand, you may alternatively pass the URI.

```python
cultural_asset.related(via="creator", with_entity_uri=person_uri)
```

> Be aware that there is no guarantee that this URI refers to a valid entity and you are
> responsible that the related entity is added to the graph.

### Mapping attributes to taxonomy (classification & material)
As any material or classification exists only once in the real world, we defined a hierarchical taxonomy for each. You can find them in the `ontology/taxonomies` folder.
If a data column contains information regarding the classification or material, you must map it to one of the entities defined in the taxonomy.
You can use the data preparation function `common.classification_and_material.detect()` to do this. This function receives an input string and returns two lists of URIs of classification and material entities.
When you add a new data source, you should check whether the function already maps the values that occur in the data source.
If values can not be mapped to any classification or material entities but know how you would map them, you can edit the rules in `etl/common/classification_and_material.py`.

For example, if in your dataset, the material `stein` occurs very often and it is not defined in the keywords, you can add it like this to the rules:
```python
 {
        "keywords": ["stone", "stoneware", "stein"],
        "classifications": [],
        "materials": ["stone"],
 },
```
Due to adding the keyword `stein` to this rule, the input `stein` will return the URI of the material entity `stone`.

This is how you can map the material and classification values to the taxonomy entities in the ETL script:
```python
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
```



### Full example

```python
from etl import etltools

# Before this: add records to the graph and save them in a list

for record in records:
    # For each record, create a CulturalAsset entity
    cultural_asset = etltools.Entity(
        identifier=record["cardId"],
        base_type="CulturalAsset",
        derived_from=record
    )

    # CSV column "Object Title" -> our schema's "title" attribute
    cultural_asset.literal(attribute="title", derived_using="objectTitle")

    # CSV column "Artist" is not empty -> create a relatedPerson entity
    if record["artist"] is not None:
        creator = etltools.Entity(
            identifier=record["cardId"] + "_creator",
            base_type="Person",
            derived_from=record
        )
        creator.literal(attribute="name", derived_using="artist")
        cultural_asset.related(via="creator", with_entity=creator)

    graph += cultural_asset.to_graph()
```

> If you need to implement more complex data preparation methods to handle your data, create a preparation folder and add your preparation functions there.

## Helpers for URI generation

```python
from etl import etltools

etltools.uris.jdcrp("foobar")
# https://graph.jdcrp.org/foobar

etltools.uris.raw("my_source_id", "my_path")
# https://graph.jdcrp.org/raw/my_source_id/my_path

etltools.uris.entity("my_source_id", "CulturalAsset", "123")
# https://graph.jdcrp.org/sources/my_source_id/CulturalAsset#123
```

## Proposing changes to the ontology

When working with a source and there is an attribute that doesn't fit to any literal or relation that is already defined
in the ontology, the attribute can be added to the ontology.

After every change in the ontology, you need to run `poetry run python build.py` to update the `combined_schema.ttl`.
Also run `poetry run python generate_backend_schema.py` in the backend folder to automatically generate the pydantic
backend schema based on the updated ontology.

If you change the literal attributes in `Cultural_asset.ttl`, `Person.ttl` or `Collection.ttl` it is important to also
add this attribute in the frontend. The pydantic schema in the backend is generated automatically.

Example: The attribute `shelfNumber` was added to the ontology in `Cultural_asset.ttl`.
```
jdcrp:shelfNumber
	a            rdf:Property ;
	rdfs:domain  jdcrp:CulturalAsset ;
	rdfs:range   xsd:string ;
	rdfs:label   "shelf number" ;
	rdfs:comment "The shelf number of this cultural asset in the Collection Point" .

```
Then, we also need to change `frontend/src/components/entityDetails/culturalAsset/properties.tsx` and add the following
line:
```
shelf_number: { label: 'Shelf number', type: EntryType.ATTRIBUTE },
```
