from etl import etltools, common

if __name__ == "__main__":
    df = etltools.data.csv_as_dataframe(
        source_id="err",
        file_path="Card.csv",
    )

    # remove rows where df["GettyArtist"] is not empty
    df = df[df["GettyArtist"].isnull()]

    # parse_author_column_using_openai requires a column named "author"
    df["author"] = df["Artist"].str.strip()

    # remove rows where df["author"] is empty
    df.loc[df["author"] == "Unknown", "author"] = None
    df.loc[df["author"] == "unknown", "author"] = None
    df.loc[df["author"] == "Various", "author"] = None
    df.loc[df["author"] == "various", "author"] = None
    df.loc[df["author"] == "modern", "author"] = None
    df.loc[df["author"] == "Modern", "author"] = None

    df = df[["author"]].dropna().drop_duplicates()

    cache = etltools.JsonCache("../../parse_authors_column_cache.json")
    df = common.authors.parse_author_column_using_openai(df, cache)
