
import os
import re
import json
from util.transcript_utils import group, millisec, SPACERMILLI
from moviepy.editor import VideoFileClip, concatenate_videoclips

def get_items(
  mapping,
  files
):
    items = []
    for file in files:
        path = "../tmp/stripped-conversation/" + file + ".txt"
        print(path)
        if os.path.exists(path):
            print(path)
            with open(path, "r") as f:
                stripped_conversation = f.read()
                speakers = stripped_conversation.split("||")
                for speaker in speakers:
                    print(speaker)
                    items.append(mapping[speaker])
    return items

def map(folder, groups):
    mapping = {}
    print(len(groups))
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
            mapping[transcript.strip()] = [folder, i, start, end]

    return mapping

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
            local = map(folder_name, groups)
            mapping.update(local)
            os.chdir('..')

    # print(mapping)
    return mapping


def merge(items):
    clips = []
    for item in items:
        folder = item[0]
        number = item[1]
        start = (item[2] - SPACERMILLI) / 1000
        start = 0 if start < 0 else start
        end = (item[3]  - SPACERMILLI) / 1000
        print(folder, number, start, end)
        os.chdir(folder)
        clip = VideoFileClip(f"{folder}.mp4").subclip(start, end)
        clips.append(clip)
        os.chdir('..')
    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile("merged_video.mp4")

FILES = ['bbc_news-2', 'dw_news-2', 'insider_news-2', 'todayonline-0']

if __name__ == "__main__":
    mapping = create_mapping()
    items = get_items(mapping, FILES)
    merge(items)

