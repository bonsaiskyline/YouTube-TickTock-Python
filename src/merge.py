
import os
import re
import json
from util.transcript_utils import group, millisec, SPACERMILLI
from moviepy.editor import VideoFileClip, concatenate_videoclips
import ffmpeg

def get_items(
  mapping,
  files
):
    items = []
    for file in files:
        path = "../tmp/stripped-conversation/" + file + ".txt"
        print(path)
        source = file.split("-")[0]
        if os.path.exists(path):
            with open(path, "r") as f:
                stripped_conversation = f.read()
                speakers = stripped_conversation.split("||")
                for speaker in speakers:
                    print(speaker)
                    print(mapping[speaker])
                    items.append(mapping[speaker][source])
    return items

def map(mapping, folder, groups):
    # print(len(groups))
    for i, group in enumerate(groups):
        captions = json.load(open(str(i) + '.json'))['segments']

        start = re.findall('[0-9]+:[0-9]+:[0-9]+\.[0-9]+', string=group[0])[0]
        end = re.findall('[0-9]+:[0-9]+:[0-9]+\.[0-9]+', string=group[-1])[1]
        start = millisec(start) #- SPACERMILLI
        end = millisec(end)  #- SPACERMILLI

        if captions:
            speaker = group[0].split()[-1]
            transcript = ""
            for c in captions:
                for j, word in enumerate(c['words']):
                    transcript += word["word"]
            transcript += '\n'
            key = transcript.strip()
            if key in mapping:
                print("======================")
                print("ALREADY EXISTS!!!!!!!!!!!!!!!")
                print(key)
                print("======================")
                existing = mapping[key]
                existing[folder] = [folder, i, start, end]
                mapping[key] = existing
            else:
                mapping[key] = {folder: [folder, i, start, end]}

def create_mapping():
    os.chdir('temp')
    current = os.getcwd()
    mapping = {}
    for folder_name in os.listdir(current):
        folder_path = os.path.join(current, folder_name)
        if os.path.isdir(folder_path):
            os.chdir(folder_path)
            output_file = "diarization.txt"
            groups = group(output_file)
            map(mapping, folder_name, groups)
            os.chdir('..')

    # print(mapping)
    return mapping


def merge(items):
    clips = []
    output_file = 'merged_video.mp4'

    for item in items:
        folder = item[0]
        number = item[1]
        start = (item[2] - SPACERMILLI) / 1000
        start = 0 if start < 0 else start
        end = (item[3]  - SPACERMILLI) / 1000
        print(folder, number, start, end)
        filename = f"/root/code/YouTube-TickTock-Python/src/temp/{folder}/{folder}.mp4"
        os.chdir(folder)
        video_stream = ffmpeg.input(filename, ss=(start), t=(end - start))
        audio_stream = video_stream.audio
        audio_stream = audio_stream.filter('atrim', start=0, end=(end - start))
        video_stream = video_stream.filter('scale', 1280, 720).filter('setdar', '16/9').filter('setsar', '1/1')
        clips.append(video_stream)
        clips.append(audio_stream)
        os.chdir('..')
    output_stream = ffmpeg.concat(*clips, v=1, a=1)
    output = ffmpeg.output(output_stream, output_file)
    ffmpeg.run(output)


def moviepy_merge(items):
    clips = []
    for item in items:
        folder = item[0]
        number = item[1]
        start = (item[2] - SPACERMILLI) / 1000
        start = 0 if start < 0 else start
        end = (item[3] - SPACERMILLI) / 1000
        print(folder, number, start, end)
        os.chdir(folder)
        clip = VideoFileClip(f"{folder}.mp4")
        subclip = clip.subclip(start, end)
        clips.append(subclip)
        os.chdir('..')
    for clip in clips:
        print("fps: ", clip.fps, "size: ", clip.size, "duration: ", clip.duration, "end: ", clip.end, "start: ",
              clip.start, "has_audio: ", clip.audio, "has_mask: ", clip.mask, "has_subclip: ", clip.subclip)
    final_clip = concatenate_videoclips(clips)
    print("Final clip stats")
    print("fps: ", final_clip.fps, "size: ", final_clip.size, "duration: ", final_clip.duration, "end: ", final_clip.end, "start: ",
          final_clip.start, "has_audio: ", final_clip.audio, "has_mask: ", final_clip.mask, "has_subclip: ", final_clip.subclip)
    final_clip.write_videofile("merged_video.mp4")
    final_clip.close()
    for clip in clips:
        clip.close()

FILES = ['insider_news-2', 'bbc_news-2', 'dw_news-2', 'todayonline-0']
if __name__ == "__main__":
    mapping = create_mapping()
    items = get_items(mapping, FILES)
    print(items)
    merge(items)

