"""
This module created embeddings from transcription text.
Author: bonsaiskyline
"""
import pandas as pd
import openai_utils
import util.file_utils as file_utils

TRANSCRIPTION_DIR = "temp/transcription/"
EMBEDDING_DIR = "temp/embedding/"
TXT_EXTENSION = ".txt"
EMBEDDING_MODEL = "text-embedding-ada-002"
UTF_8 = "utf-8"


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
        video_name = filename.replace(TXT_EXTENSION, "")
        with open(path, "r", encoding=UTF_8) as f:
            embedding = openai_utils.create_embedding(
                text=f.read(),
                model=EMBEDDING_MODEL
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
    transcription_filenames = file_utils.get_filenames(
        dir_path=TRANSCRIPTION_DIR,
        extension=TXT_EXTENSION
    )
    embeddings_df = get_embeddings_df(
        filenames=transcription_filenames,
        path_prefix=TRANSCRIPTION_DIR
    )
    embeddings_df.to_csv(
        EMBEDDING_DIR + "embeddings.csv",
        index=False
    )
