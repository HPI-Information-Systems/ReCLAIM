import openai
import pandas as pd


def prepare_df_for_embedding(
    df: pd.DataFrame, df_col_to_embed_name: str
) -> pd.DataFrame:
    new_df = df.drop_duplicates(subset=df_col_to_embed_name, inplace=False)
    new_df = new_df.dropna(subset=[df_col_to_embed_name], inplace=False)
    return new_df


def generate_embeddings(df_col_to_embed: pd.Series, embedding_model: str) -> pd.Series:
    return df_col_to_embed.apply(
        lambda hao_val: openai.embeddings.create(input=hao_val, model=embedding_model)
        .data[0]
        .embedding
    )
