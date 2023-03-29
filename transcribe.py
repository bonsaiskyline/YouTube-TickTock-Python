import openai_utils
import os

MAX_MP4_SIZE = 26214400
VIDEO_DIR_PATH = "./video/"
MP4_EXTENSION = ".mp4"
TRANSCIPTION_DIR = "./transcription/"


def get_mp4_filenames(
        dir_path: str
):
    """
    Gets mp4 filenames.

    Args:
        dir_path (str): Path to directory.

    Returns:
        list: List of mp4 files.
    """
    return [f for f in os.listdir(dir_path) if f.endswith(MP4_EXTENSION)]


def transcribe_audio(
        source_path: str,
        destination_path: str
):
    """
    Transcribes audio.

    Args:
        source_path (str): Path to source audio.
        destination_path (str): Path to destination transcription.
    """
    if not os.path.isfile(destination_path):
        with open(destination_path, 'w') as output:
            transcript = openai_utils.transcribe_audio(source_path)
            output.write(transcript.text)
            print("Transcribed " + source_path)


def get_transcription_path(
        video_filename: str
):
    """
    Gets the path to the transcription of a video.

    Args:
        video_filename (str): Filename of video.

    Returns:
        str: Path to transcription.
    """
    transcription_filename = video_filename.replace(
        MP4_EXTENSION,
        '.txt'
    )
    return TRANSCIPTION_DIR + transcription_filename


def transcribe_mp4_audio(
        mp4_filenames: list
):
    """
    Transcribes videos.
    """
    for mp4_filename in mp4_filenames:
        mp4_path = VIDEO_DIR_PATH + mp4_filename
        mp4_filesize = os.path.getsize(mp4_path)
        if mp4_filesize < MAX_MP4_SIZE:
            transcription_path = get_transcription_path(mp4_filename)
            transcribe_audio(
                source_path=mp4_path,
                destination_path=transcription_path
            )
        else:
            print("Skipping " + mp4_filename + " because it is " +
                  str(mp4_filesize) + " bytes and the max is " + str(MAX_MP4_SIZE) + " bytes.")


if __name__ == "__main__":
    mp4_filenames = get_mp4_filenames(
        dir_path=VIDEO_DIR_PATH
    )
    transcribe_mp4_audio(
        mp4_filenames=mp4_filenames
    )
