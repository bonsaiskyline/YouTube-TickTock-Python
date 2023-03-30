import os
import json

def create_conversations_from_speakers(
  input_filename: str
) -> dict:
    """
    Creates conversations from speakers.

    Args:
        transcript (str): Transcript of conversation.

    Returns:
        list: List of conversations.
    """
    lines = open(input_filename).read().split("\n")
    conversations = []
    current_conversation = []

    speakers = set()
    prev_speaker = None

    for i in range(0, len(lines) - 1, 2):
        speaker = lines[i].strip()
        message = lines[i + 1].strip()

        if prev_speaker is None:
            prev_speaker = speaker

        if speaker not in speakers:
            if len(speakers) == 2:
                conversations.append(current_conversation)
                current_conversation = []
                speakers.clear()

            speakers.add(speaker)

        line = f"{speaker}: {message}"

        if len(speakers) <= 2:
            current_conversation.append(line)
        else:
            conversations.append(current_conversation)
            speakers.remove(prev_speaker)
            current_conversation = [line]

        prev_speaker = speaker

    if current_conversation:
        conversations.append(current_conversation)

    return {"conversations": conversations}

if __name__ == "__main__":
    os.chdir('temp')
    current = os.getcwd()
    for folder_name in os.listdir(current):
        folder_path = os.path.join(current, folder_name)
        if os.path.isdir(folder_path):
            os.chdir(folder_path)
            print(f"Creating conversations in: {folder_name}")
            conversations = create_conversations_from_speakers(
              input_filename="transcript.txt"
            )
            with open('conversations.json', 'w') as f:
              f.write(json.dumps(conversations, indent=4))
            os.chdir('..')
