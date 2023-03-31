
import os
import re
import json
from util.transcript_utils import group

def print_transcript(groups):
    gidx = -1
    transcript = ""
    for g in groups:
        gidx += 1
        captions = json.load(open(str(gidx) + '.json'))['segments']

        if captions:
            speaker = g[0].split()[-1]
            transcript += f"==> {speaker}: \n"

            for c in captions:
                for i, w in enumerate(c['words']):
                    if w == "":
                        continue
                    transcript += w["word"]
            transcript += '\n'
    return transcript

os.chdir('temp')
current = os.getcwd()
for folder_name in os.listdir(current):
    folder_path = os.path.join(current, folder_name)
    if os.path.isdir(folder_path):
        os.chdir(folder_path)

        print(f"Folder found: {folder_name}")
        output_file = "diarization.txt"
        groups = group(output_file)
        transcript = print_transcript(groups)
        print(transcript)
        with open('transcript.txt', 'w') as f:
            f.write(transcript)
        os.chdir('..')