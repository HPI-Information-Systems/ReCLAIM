from enum import Enum
from typing import List
from backend.parsing.entity_parser.create_entity import (
    extract_entity_data_from_db_response,
)
from backend.parsing.utility import (
    extract_entity_id_from_uri,
    extract_source_id_from_uri,
)
from backend.schema import Collection, CulturalAsset, Person
from backend.schema.base_schema import SearchResults, SupportedSource
from backend.topics import get_basic_search_topic, get_cultural_asset_topics
from fastapi import HTTPException, status
from neo4j import Session
import re

# The delimiter needs to be the same as in the frontend
URL_SEARCH_FIELD_DELIMITER = "|"


class SearchEntityType(Enum):
    """
    Defines the available entity types for search, mapping their name to the backend class type
    """

    CulturalAsset = CulturalAsset
    Person = Person
    Collection = Collection


def escape_lucene_special_characters(query_part: str) -> str:
    """
    Function to escape lucene query special characters by adding a backslash
    See https://lucene.apache.org/core/6_0_0/queryparser/org/apache/lucene/queryparser/classic/package-summary.html#Escaping_Special_Characters
    """
    return re.sub(r"([+\-&|!(){}[\]^\"~*?:\\/])", r"\\\1", query_part)


def get_lucene_query(
    search_text: str,
    attributes: List[str],
    is_contains_not: bool,
    use_fuzzy_search: bool,
    search_entire_words_only: bool,
) -> str:
    """
    Compose and escape the lucene query string for the given search text and search attribute.

    :param search_text: The search text
    :param attributes: The list of attributes to search in. If empty, the search is performed on all attributes.
    :param is_contains_not: If True, the search is negated (i.e. NOT search_text)
    :param use_fuzzy_search: If True, the search is performed with fuzzy search
    :return: The lucene query string
    """

    search_text = escape_lucene_special_characters(search_text)
    if search_text == "":
        search_text = "*"

    lucene_query = ""

    if use_fuzzy_search:
        search_text = " ".join([f"{word}~" for word in search_text.split(" ")])

    if not search_entire_words_only:
        search_text = f"*{search_text}*"

    if len(attributes) == 0:
        lucene_query += f'({search_text}) OR ("{search_text}")'
    else:
        lucene_query += " OR ".join(
            [
                f'{attribute}:({search_text}) OR {attribute}:("{search_text}")'
                for attribute in attributes
            ]
        )
    # Lucene queries have the restriction that they can't consist of only NOT queries. At least one query has to be a positive query.
    # Therefore, in case of a is_contains_not query, we add "* AND NOT ..." to the query.
    if is_contains_not:
        lucene_query = "* AND NOT (" + lucene_query + ")"
    return lucene_query


def raise_search_query_error(error_message: str):
    print(error_message)
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=error_message,
    )


def get_search_entity_fulltext_query(
    subquery_id: int,
    query_params: dict,
    search_entity_type: SearchEntityType,
    lucene_query: str,
):
    """
    Returns a Cypher query for a fulltext index query against the search entity type (i.e. the entity type which is displayed in the search results).
    The query parameters required are added to the query_params dictionary.

    :param subquery_id: A unique identifier for the subquery that must be unique within the top-level query
    :param query_params: The dictionary to which the query parameters should be added, which is then passed to neo4j
    :param search_entity_type: The entity type for which the search is performed and displayed in the search results
    :param lucene_query: The lucene query string
    :return: The Cypher query string
    """

    # Validate that search_entity_type is one of the allowed types
    if search_entity_type not in SearchEntityType:
        raise_search_query_error(f"Invalid search entity type: {search_entity_type}.")

    param_name_fulltext_index = f"fulltextIndex_{str(subquery_id)}"
    param_name_lucene_query = f"luceneQuery_{str(subquery_id)}"

    query_params[param_name_fulltext_index] = search_entity_type.name + "FulltextIndex"
    query_params[param_name_lucene_query] = lucene_query

    return f"""
        CALL db.index.fulltext.queryNodes(${param_name_fulltext_index}, ${param_name_lucene_query}) YIELD node AS search_entity, score
        WHERE ANY(source_identifier IN $sources WHERE search_entity.uri CONTAINS source_identifier) OR $sources = []
        RETURN search_entity, score
    """


def get_foreign_search_entity_fulltext_query(
    subquery_id: int,
    query_params: dict,
    foreign_search_entity_type: str,
    search_entity_type: SearchEntityType,
    lucene_query: str,
):
    """
    Returns a Cypher query for a fulltext index query against a foreign entity type (i.e. not the entity type which is displayed in the search results).
    The query parameters required are added to the query_params dictionary.

    :param subquery_id: A unique identifier for the subquery that must be unique within the top-level query
    :param query_params: The dictionary to which the query parameters should be added, which is then passed to neo4j
    :param foreign_search_entity_type: The foreign entity type for which the fulltext index should be queried
    :param search_entity_type: The entity type for which the search is performed and displayed in the search results
    :param lucene_query: The lucene query string
    :return: The Cypher query string
    """

    # Validate that search_entity_type is one of the allowed types
    # Most importantly, this prevents a Cypher injection, since the search_entity_type can not be passed to the query as a parameter.
    if search_entity_type not in SearchEntityType:
        raise_search_query_error(f"Invalid search entity type: {search_entity_type}.")

    param_name_fulltext_index = f"fulltextIndex_{str(subquery_id)}"
    param_name_lucene_query = f"luceneQuery_{str(subquery_id)}"

    query_params[param_name_fulltext_index] = (
        foreign_search_entity_type + "FulltextIndex"
    )
    query_params[param_name_lucene_query] = lucene_query

    return f"""
        CALL db.index.fulltext.queryNodes(${param_name_fulltext_index}, ${param_name_lucene_query}) YIELD node AS entity, score
        MATCH (entity)-[]-(search_entity:`jdcrp__{search_entity_type.name}`)
        WHERE ANY(source_identifier IN $sources WHERE search_entity.uri CONTAINS source_identifier) OR $sources = []
        RETURN search_entity, score
    """


def parse_search_query(
    search_query_list: List[str],
    search_entity_type: SearchEntityType,
    query_params: dict,
) -> List[str]:
    """
    Parses the search query list and returns a list of Cypher subqueries for the search.
    NOTICE: Will be updated (and thereby simplified) in the near future with regard to the new topics feature.

    :param search_query_list: List of search queries. Each query is a string in the format [!][topic]|<search_text>. See backend/topics.py.
    :param search_entity_type: The entity type to search for
    :param query_params: The dictionary to which the query parameters should be added, which is then passed to neo4j
    :return: A list of Cypher subqueries for the search
    """

    # The lucene query parts for the cultural asset, which are joined together with an AND
    cypher_subqueries: list[str] = []

    # Used to keep track of the subquery id, for the prepared statement names
    query_id = 0

    for query in search_query_list:

        topic_cypher_queries: list[str] = []

        is_contains_not = False
        if len(query) > 0 and query[0] == "!":
            is_contains_not = True
            query = query[1:]

        query_parts = query.split(URL_SEARCH_FIELD_DELIMITER)
        if len(query_parts) < 1:
            raise_search_query_error(
                f"Too few arguments ({str(len(query_parts))}/1) for query: '{query}'. Expected format: [!][topic]|<search_text>"
            )
        if len(query_parts) > 2:
            raise_search_query_error(
                f"Too many arguments ({len(query_parts)}/2) for search query: '{query}'. Expected format: [!][topic]|<search_text>"
            )

        query_text = ""
        topic = None

        if len(query_parts) == 1:
            query_text = query_parts[0]
            topic = get_basic_search_topic()
        else:
            query_topic_name = query_parts[0]
            query_text = query_parts[1]

            # Get the list of search attributes for the given topic
            match search_entity_type:
                case SearchEntityType.CulturalAsset:
                    topic = get_cultural_asset_topics().get(query_topic_name)
                case SearchEntityType.Person:
                    pass
                case SearchEntityType.Collection:
                    pass
            if topic is None:
                raise_search_query_error(f"Invalid search topic: '{query_topic_name}'.")

        for entity_type, attributes in topic.searched_attributes.items():
            lucene_query = get_lucene_query(
                query_text, attributes, is_contains_not, False, True
            )

            if entity_type != search_entity_type.name:
                # Foreign entity query
                topic_cypher_queries.append(
                    get_foreign_search_entity_fulltext_query(
                        query_id,
                        query_params,
                        entity_type,
                        search_entity_type,
                        lucene_query,
                    )
                )
            else:
                # Search entity query
                topic_cypher_queries.append(
                    get_search_entity_fulltext_query(
                        query_id,
                        query_params,
                        search_entity_type,
                        lucene_query,
                    )
                )

            query_id += 1

        # Remove duplicates and only return the result with the highest score
        # Within a topic, the number of times an entity is found does not count
        topic_cypher_query = (
            "CALL {"
            + " UNION ALL ".join(topic_cypher_queries)
            + "}"
            + """
            RETURN search_entity, MAX(score) AS score
            """
        )
        cypher_subqueries.append(topic_cypher_query)

    return cypher_subqueries


def execute_search_query(
    search_query_list: List[str],
    search_entity_type: SearchEntityType,
    limit: int,
    cursor: int,
    session: Session,
    filters: dict = None,
):
    """
    Execute a search query and return the results.

    :param search_query_list: List of search queries. Each query is a string in the format [!][topic]|<search_text>
    :param search_entity_type: The entity type to search for
    :param limit: The maximum number of results to return
    :param cursor: The offset for the search results
    :param session: The neo4j session
    :return: The raw search response from the database
    """

    query_params: dict = {}

    query_params["sources"] = (
        filters.get("sources") if filters is not None and filters.get("sources") else []
    )

    cypher_subqueries = parse_search_query(
        search_query_list, search_entity_type, query_params
    )

    if len(cypher_subqueries) == 0:
        raise_search_query_error("No search queries were provided.")

    query_params["cursor"] = cursor
    query_params["limit"] = limit
    query_params["num_search_filters"] = len(cypher_subqueries)

    cypher_query = (
        "CALL {"
        + " UNION ALL ".join(cypher_subqueries)
        + "}"
        + """
        WITH search_entity, score
        ORDER BY score DESC
        """
    )

    # Only count the occurrences for queries with actually more than one subqueries
    # Omitting this saves time
    if len(cypher_subqueries) != 1:
        cypher_query += """
        WITH apoc.coll.frequencies(COLLECT(search_entity)) AS count_entity_occurrences
        UNWIND count_entity_occurrences AS entity_with_count
        WITH entity_with_count.item AS search_entity, entity_with_count.count AS num_occurrences
        ORDER BY num_occurrences DESC
        %s MATCH (search_entity)-[image_relation]->(image:jdcrp__Image)
        WITH search_entity, num_occurrences, $num_search_filters AS num_search_filters,
        COLLECT({
              relation: type(image_relation),
              related_entity: {
                  attributes: properties(image)
              }
          }) AS image_relations
        WITH COLLECT({
            attributes: properties(search_entity),
            relations: image_relations,
            is_match_all_filters: num_occurrences = num_search_filters
        }) AS all_entities
        RETURN
            all_entities[$cursor..$cursor+$limit] AS entities,
            size([entity IN all_entities WHERE entity.is_match_all_filters]) AS total_count_match_all_search_filters,
            size([entity IN all_entities WHERE NOT entity.is_match_all_filters]) AS total_count_match_some_search_filters
        """ % (
            "" if filters is None or filters.get("onlyWithImages") else "OPTIONAL "
        )
    else:
        cypher_query += """
        %s MATCH (search_entity)-[image_relation]->(image:jdcrp__Image)
        WITH search_entity,
            COLLECT({
                relation: type(image_relation),
                related_entity: {
                    attributes: properties(image)
                }
            }) AS image_relations
        WITH COLLECT({
            attributes: properties(search_entity),
            relations: image_relations,
            is_match_all_filters: true
        }) AS all_entities
        RETURN
            all_entities[$cursor..$cursor+$limit] AS entities,
            size(all_entities) AS total_count_match_all_search_filters,
            0 AS total_count_match_some_search_filters
        """ % (
            "" if filters is None or filters.get("onlyWithImages") else "OPTIONAL"
        )

    return session.run(
        cypher_query,
        query_params,
    ).data()[0]


def search(
    search_query_list: List[str],
    search_entity_type: SearchEntityType,
    limit: int,
    cursor: int,
    session: Session,
    filters: dict = None,
):
    """
    Search for entities of the given search_entity_type with queries search_query_list.

    :param search_query_list: List of search queries. Each query is a string in the format [!][topic]|<search_text>
    :param search_entity_type: The entity type to search for
    :param limit: The maximum number of results to return
    :param cursor: The offset for the search results
    :param session: The neo4j session
    :return: The search results
    """

    db_response = execute_search_query(
        search_query_list,
        search_entity_type,
        limit=limit,
        cursor=cursor,
        session=session,
        filters=filters,
    )

    search_entity_class = search_entity_type.value
    results_match_all_search_filters = []
    results_match_some_search_filters = []

    for db_entity in db_response["entities"]:
        entity_uri = db_entity["attributes"]["uri"]

        entity_parsed = search_entity_class(
            id=extract_entity_id_from_uri(entity_uri),
            source_id=SupportedSource(extract_source_id_from_uri(entity_uri)),
            **extract_entity_data_from_db_response(search_entity_class, db_entity),
        )

        if db_entity["is_match_all_filters"]:
            results_match_all_search_filters.append(entity_parsed)
        else:
            results_match_some_search_filters.append(entity_parsed)

    return SearchResults[search_entity_class](
        results_match_all_search_filters=results_match_all_search_filters,
        results_match_some_search_filters=results_match_some_search_filters,
        total_count_match_all_search_filters=db_response[
            "total_count_match_all_search_filters"
        ],
        total_count_match_some_search_filters=db_response[
            "total_count_match_some_search_filters"
        ],
    )
