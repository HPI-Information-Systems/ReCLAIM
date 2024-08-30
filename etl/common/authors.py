from etltools import JsonCache
import json
import openai
import pandas as pd
from openai.types.chat import (
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
)

# OpenAI API key
openai.api_key = "xxx"

# df needs to have an "author" column
def parse_author_column_using_openai(
    df: pd.DataFrame, cache: JsonCache
) -> pd.DataFrame:
    '''
    This function uses OpenAI's Chat API to parse the "author" column of the input DataFrame.

    The function sends the data in batches to OpenAI, and caches the results in a JsonCache object.
    The complex input of the authors column is parsed and divided into the following fields:
    name, pseudonym, styleOfStr, dateStr, locationStr.
    '''
    df = df.dropna(subset=["author"])

    system_message = ChatCompletionSystemMessageParam(
        role="system",
        content="""You are an expert in artwork history. We found a dataset of thousands of artworks, but the data is messy. Your task is to look specifically at the values of the "authors" column -- some of them aren't real persons but instead locations (countries/cities/regions) or dates (18. Jhdt, etc.)
Only extract information that is directly inferable from the text, don't use any external knowledge.
Note that some of the values may contain typos, you should keep them since they might provide historic relevance (this does not apply for unnecessary double spaces, dots, etc).

For each of the rows, respond with a JSON object that matches the following schema:
{ "row": string, "name": string|null, "pseudonym": string|null, "styleOfStr": string|null, "dateStr": string|null, "locationStr": string|null}.

Some hints:
- Some artists have a pseudonym, that shouldn't be part of their "name" but of the "pseudonym" field.
- "the Elder", "d.Ä.", "der Jüngere" etc. should be part of the "name" field, but ALWAYS put such suffixes at the end.
- Sometimes a mentioned artist isn't the actual creator of the artwork, but instead inspired it ("style of", "after", "Workshop", etc.). In that case, use that artist's name in the "styleOfStr" field, not in the "name".
- When a century is mentioned in a weird format, like "5 cent" or "15/cent", record it as "5th cent." or "15th cent.".

Here are some examples:
Input: "Persian, 17th cent."
Output: { "row": "Persian, 17th cent.", "name": null, "pseudonym": null, "styleOfStr": null, "dateStr": "17th cent.", "locationStr": "Persian"}

Input: "about 1680"
Output: { "row": "about 1680", "name": null , "pseudonym": null, "styleOfStr": null, "dateStr": "about 1680", "locationStr": null}

Input: "Riemenschneider, Tilman"
Output: { "row": "Riemenschneider, Tilman", "name": "Tilman Riemenschneider", "pseudonym": null, "styleOfStr": null, "dateStr": null, "locationStr": null}

Input: "Byzantine 4 cent."
Output: { "row": "Byzantine 4th cent.", "name": null , "pseudonym": null, "styleOfStr": null, "dateStr": "4th cent.", "locationStr": "Byzantine"}

Input: "Cranach, Lucas the Elder"
Output: { "row": "Cranach, Lucas the Elder", "name": "Lucas Cranach the Elder", "pseudonym": null, "styleOfStr": null, "dateStr": null, "locationStr": null}

Input: "Luca della Robbia Work-shop"
Output: { "row": "Luca della Robbia Work-shop", "name": null, "pseudonym": null, "styleOfStr": "Luca della Robbia", "dateStr": null, "locationStr":

Input: "Fra Giovanni da Fiesole, called Angelico":
Output:  {"row": "Fra Giovanni da Fiesole, called Angelico", "name": "Fra Giovanni da Fiesole", "pseudonym": "Angelico", "styleOfStr": null, "dateStr": null, "locationStr": null}

Input: "Caravaggio"
Output: {"row": "Caravaggio", "name": "Caravaggio", "pseudonym": null, "styleOfStr": null, "dateStr": null, "locationStr": null }

Input: "Luca della Robbia, Style of"
Output: {"row": "Luca della Robbia, Style of", "name": null, "pseudonym": null, "styleOfStr": "Luca della Robbia", "dateStr": null, "locationStr": null}

Respond directly with the one large JSON array, nothing else. NEVER precede your response with any other text or syntax information (e.g. ```json ...```).
The array should look like [{"row": ... }, {"row": ... }, ...]
""",
    )

    batch_size = 50

    for i in range(0, len(df), batch_size):
        batch = df.iloc[i : i + batch_size]

        filtered_batch = batch[
            batch.apply(lambda row: not cache.has(row["author"]), axis=1)
        ]
        if len(filtered_batch) == 0:
            continue

        authors_json = filtered_batch["author"].to_json(orient="records")
        user_message = ChatCompletionUserMessageParam(
            role="user",
            content="Here are the authors I want to parse:\n\n" + authors_json,
        )

        print("Sending batch", i, "to", i + batch_size, "to OpenAI")
        print(user_message["content"])

        response = openai.chat.completions.create(
            model="gpt-4-turbo-preview",
            # model="gpt-3.5-turbo",
            temperature=0,
            messages=[system_message, user_message],
        )

        print(response.usage)

        content = response.choices[0].message.content

        # parse content as JSON
        try:
            if content.startswith("```json"):
                content = content[7:-3]

            parsed = json.loads(content)
        except json.JSONDecodeError as e:
            print("Error parsing JSON:", e)
            continue

        for parsed_row in parsed:
            cache.set(parsed_row["row"], parsed_row)

        cache.write()
        print("\n\n")

    return df
