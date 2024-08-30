# Event Extraction

In order to make the provenance history of cultural assets searchable, we store event entities in the database. These are created using event extraction from provenance describing data columns. For extracting structured events from raw data sources, we apply different techniques, depending on the format of the provenance describing texts. We highly recommend reading the bachelor thesis about event extraction to develop an understanding in the field.

This directory contains functions for analyzing the provenance descriptions of a dataset and for generating few-shot examples. `analyze_dataset.ipynb` includes a small example for the WCCP dataset. The `event_types.json` file contains the current event schema with detailed descriptions.

Upon closer analysis of a specific dataset, you should decide if a rule-based approach or the use of an LLM is applicable. Rule-based approaches should be directy implemented in the corresponding ETL script. When an LLM is used, you should create an `event_extraction` directory in the corresponding ETL directory (see wiesbaden ETL directory). This `event_extraction` directory should then contain:
- a script that utlizes functions from this directory (see `wccp.ipynb`)
- the source-specific prompt
- if necessary, manually labeled few-shot examples
- a JSON cache with the results (the result cache can then be used by the corresponding ETL script, to create event entities)


## The state of EE in different data sources

So far, we developed a technique for extracting events in the WCCP dataset and also made some progress in extracting events in the Linz dataset.

**EE in the WCCP dataset**

In the WCCP dataset, the provenance describing columns are "history-and-ownership", "depot-possessor", "depot-number", "arrival-condition", "condition-and-repair-record", "arrival-date" and "exit-date". The "histoy-and-ownership" field contains the main provenance description in form of a few natural language sentences. The other fields contain single strings and supplement the main provenance description. Since the main provenance description is mainly unstructured and the other fields often contain different information to what the column name states, we used GPT-4 to infer structured events. This process is documented in the bachelor-thesis about event extraction.

**EE in the Linz dataset**

In the Linz dataset, the provenance describing column is named "Ereignisse". The "Ereignisse" column is semi-structured. The text contains key-value pairs that are seperated by line breaks. Each key-value pair usually describes one event. The value contains single words, but also whole sentences. By filtering out the keys, we are able to create an event for each key-value pair where only the "description" field of the event is set. This means that the event argument extraction is still missing. Here, it would be possible to use LLM prompts as in the WCCP dataset. However the source specific information of the prompt must be adapted.

**EE in further datasets**

Also the Munich, ERR and Marbug datasets contain columns that describe the provenance of cultural assets:

- Munich contains the "herkunft/verbleib/sozietät" column that contains short sentences, describing the provenance.
- ERR contains the "PostConfiscationHistory" column that contains short sentences, describing the provenance.
- Marburg also contains a "history-and-ownership" column (as in WCCP). However this dataset only contains 58 unique provenance descriptions and the descriptions are often very illegible. Therefore manual parsing could be applied here.

For each dataset, a manual analysis of the text structure in the provenance describing columns is necessary to choose a specific EE technique.

## EE to empower the search

We divided the advanced search into topics, where each topic is a group of entity attributes that are jointly searched. So far, each event type is represented by a topic in the adcanced search, so that it is not possible to distinguish between event attributes. This has two implications:
1. Applying only Event Detection, in which event triggers are identified and classified from the free text, is sufficient to make the provenance description searchable (see state of EE in Linz)
2. Creating a seperated interface for searching provenance descriptions should be considered to search for specific event arguments.
