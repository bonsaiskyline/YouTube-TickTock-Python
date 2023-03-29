"""
This module does something cool that helps with X.
Author: [your name]
"""
import os
import pandas as pd
import openai_utils


def get_transcription_filenames():
    """
    Returns:
            list: List of transcription files.
    """
    return [f for f in os.listdir("./transcription") if f.endswith(".txt")]


def get_embeddings_df(
    filenames,
    path_prefix
):
    """
    Get embeddings from text files.

    Args:
            filenames (list): List of filenames.
            path_prefix (str): Path prefix.

    Returns:
            pd.DataFrame: Dataframe of embeddings.
    """
    dfs = []
    for filename in filenames:
        path = path_prefix + filename
        video_name = filename.replace(".txt", "")
        with open(path, "r", encoding="utf-8") as f:
            embedding = openai_utils.create_embedding(
                text=f.read(),
                model="text-embedding-ada-002"
            )
            dfs.append(
                pd.DataFrame(
                    [[
                        video_name,
                        embedding
                    ]],
                    columns=[
                        "video_name",
                        "embedding"
                    ]
                )
            )
    return pd.concat(dfs, axis=0)


if __name__ == "__main__":
    transcription_filenames = get_transcription_filenames()
    embeddings_df = get_embeddings_df(
        filenames=transcription_filenames,
        path_prefix="./transcription/"
    )
    embeddings_df.to_csv(
        "embedding/embeddings.csv",
        index=False
    )
