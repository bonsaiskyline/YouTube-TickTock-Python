"""
This module strips conversations.
Author: bonsaiskyline
"""
import util.file_utils as file_utils
import json

CONVERSATION_DIR = "tmp/conversation/"
EMBEDDING_DIR = "tmp/embedding/"
JSON_EXTENSION = ".json"
EMBEDDING_MODEL = "text-embedding-ada-002"
UTF_8 = "utf-8"


def strip_conversations(
    filenames,
    path_prefix
):
  for filename in filenames:
    path = path_prefix + filename
    with open(path, "r", encoding=UTF_8) as input_file:
      conversations = json.load(input_file)["conversations"]
      print(conversations)
      for i, conversation in enumerate(conversations):
        print(conversation)
        stripped_lines = [line.split(":: ")[1] for line in conversation]
        result = " ".join(stripped_lines)
        conversation_name = filename.replace(JSON_EXTENSION, "") + "-" + str(i)
        with open("tmp/stripped-conversation/" + conversation_name + ".txt", 'w') as output:
          output.write(result)

if __name__ == "__main__":
    conversation_filenames = file_utils.get_filenames(
        dir_path=CONVERSATION_DIR,
        extension=JSON_EXTENSION
    )
    stripped_conversations = strip_conversations(
        filenames=conversation_filenames,
        path_prefix=CONVERSATION_DIR
    )
