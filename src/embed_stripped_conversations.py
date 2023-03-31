"""
This module creates embeddings from conversations.
Author: bonsaiskyline
"""
import pandas as pd
import openai_utils
import util.file_utils as file_utils
import json

STRIPPED_CONVERSATION_DIR = "tmp/stripped-conversation/"
EMBEDDING_DIR = "tmp/embedding/"
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
        with open(path, "r", encoding=UTF_8) as f:
            conversation = f.read()
            embedding = openai_utils.create_embedding(
                text=conversation,
                model=EMBEDDING_MODEL
            )
            name = filename.replace(TXT_EXTENSION, "")
            print(name)
            print(conversation)
            dfs.append(
                pd.DataFrame(
                    [[
                        name,
                        embedding
                    ]],
                    columns=[
                        "name",
                        "embedding"
                    ]
                )
            )

    return pd.concat(dfs, axis=0)


if __name__ == "__main__":
    filenames = file_utils.get_filenames(
        dir_path=STRIPPED_CONVERSATION_DIR,
        extension=TXT_EXTENSION
    )
    embeddings_df = get_embeddings_df(
        filenames=filenames,
        path_prefix=STRIPPED_CONVERSATION_DIR
    )
    embeddings_df.to_csv(
        EMBEDDING_DIR + "conversation-embeddings.csv",
        index=False
    )
