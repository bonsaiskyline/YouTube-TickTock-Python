import openai
import os

openai.api_key = os.environ['OPENAI_API_KEY']

def transcribe(filename):
  f = open(filename, 'rb')
  transcript = openai.Audio.transcribe("whisper-1", f)
  return transcript

MAX_VIDEO_SIZE = 26214400

for video_filename in os.listdir("./video"):
  if video_filename.endswith(".mp4"):
    video_path = "./video/" + video_filename
    video_filesize = os.path.getsize(video_path)
    if video_filesize >= 26214400:
      print(video_filename + " is " + str(video_filesize) + " bytes. Max is " + str(MAX_VIDEO_SIZE) + " bytes.")
      continue
    transcription_filename = video_filename.replace('.mp4', '.txt')
    transcription_path = "./transcription/" + transcription_filename
    if not os.path.isfile(transcription_path):
      with open(transcription_path, 'w') as output:
        print(video_filename)
        transcript = transcribe(video_path)
        output.write(transcript.text)