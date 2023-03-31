"""
This module creates embeddings from conversations.
Author: bonsaiskyline
"""
import pandas as pd
import openai_utils
import util.file_utils as file_utils
import json

CONVERSATION_DIR = "tmp/conversation/"
EMBEDDING_DIR = "tmp/embedding/"
JSON_EXTENSION = ".json"
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
            conversations = json.load(f)["conversations"]
            for i, conversation in enumerate(conversations):
                stripped_lines = [line.split(":: ")[1]
                                  for line in conversation]
                result = " ".join(stripped_lines)
                embedding = openai_utils.create_embedding(
                    text=result,
                    model=EMBEDDING_MODEL
                )
                conversation_name = filename.replace(JSON_EXTENSION, "") + "-" + str(i)
                with open("tmp/stripped-conversation/" + conversation_name + ".txt", 'w') as output:
                  output.write(result)
                print(conversation_name)
                print(result)
                dfs.append(
                    pd.DataFrame(
                        [[
                            conversation_name,
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
    conversation_filenames = file_utils.get_filenames(
        dir_path=CONVERSATION_DIR,
        extension=JSON_EXTENSION
    )
    embeddings_df = get_embeddings_df(
        filenames=conversation_filenames,
        path_prefix=CONVERSATION_DIR
    )
    embeddings_df.to_csv(
        EMBEDDING_DIR + "conversation-embeddings.csv",
        index=False
    )
