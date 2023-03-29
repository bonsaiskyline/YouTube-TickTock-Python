"""
Gets the configured OpenAI module.
Author: bonsaiskyline
"""
import os
import openai


def get_openai():
    """
    Returns:
            openai: The configured OpenAI module.
    """
    openai.api_key = os.environ['OPENAI_API_KEY']
    return openai


def transcribe_audio(
    filename: str
):
    """
        Args:
            filename (str): Filename of audio file.

        Returns:
            openai.Audio: Transcribed audio.
    """
    buffered_reader = open(
        filename,
        'rb'
    )
    transcript = get_openai().Audio.transcribe(
        "whisper-1",
        buffered_reader
    )
    return transcript


def create_embedding(
    text: str,
    model="text-embedding-ada-002"
):
    """
    Get embedding from text.

    Args:
          text (str): Text to embed.
          model (str): Model to use for embedding. Defaults to "text-embedding-ada-002".

    Returns:
          list: Embedding vector.
     """
    text = text.replace("\n", " ")
    response = get_openai().Embedding.create(
        input=[text],
        model=model
    )
    return response['data'][0]['embedding']
