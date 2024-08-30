def sanitize_cypher_query_label(query_label: str) -> str:
    """
    Sanitize Cypher Query User Input
    See https://neo4j.com/developer/kb/protecting-against-cypher-injection/
    """
    return "`" + (query_label.replace("\\", "\\\\").replace("`", "``")) + "`"
