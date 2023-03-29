import openai_utils
import os


MAX_VIDEO_SIZE = 26214400
VIDEO_PATH_PREFIX = "./video/"
TRANSCIPTION_PATH_PREFIX = "./transcription/"


def transcribe_videos():
    """
    Transcribes videos.
    """
    for video_filename in os.listdir(VIDEO_PATH_PREFIX):
        if video_filename.endswith(".mp4"):
            video_path = VIDEO_PATH_PREFIX + video_filename
            video_filesize = os.path.getsize(video_path)
            if video_filesize >= MAX_VIDEO_SIZE:
                print(video_filename + " is " + str(video_filesize) +
                      " bytes. Max is " + str(MAX_VIDEO_SIZE) + " bytes.")
                continue
            transcription_filename = video_filename.replace('.mp4', '.txt')
            transcription_path = TRANSCIPTION_PATH_PREFIX + transcription_filename
            if not os.path.isfile(transcription_path):
                with open(transcription_path, 'w') as output:
                    print(video_filename)
                    transcript = openai_utils.transcribe_audio(video_path)
                    output.write(transcript.text)


if __name__ == "__main__":
  transcribe_videos()
