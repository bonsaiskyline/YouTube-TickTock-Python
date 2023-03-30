
import os
import re
import json

SPACERMILLI = 2000
def millisec(timeStr):
    spl = timeStr.split(":")
    s = (int)((int(spl[0]) * 60 * 60 + int(spl[1]) * 60 + float(spl[2]) )* 1000)
    return s

def group(filename):
    dzs = open(filename).read().splitlines()
    groups = []
    g = []
    lastend = 0

    for d in dzs:
        if g and (g[0].split()[-1] != d.split()[-1]):      #same speaker
            groups.append(g)
            g = []

        g.append(d)

        end = re.findall('[0-9]+:[0-9]+:[0-9]+\.[0-9]+', string=d)[1]
        end = millisec(end)
        if (lastend > end):       #segment engulfed by a previous segment
            groups.append(g)
            g = []
        else:
            lastend = end

    if g:
        groups.append(g)
    print(*groups, sep='\n')
    return groups

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
        # if (folder_name == 'the_hot_box'):
        #     continue
        output_file = "diarization.txt"
        groups = group(output_file)
        transcript = print_transcript(groups)
        print(transcript)
        with open('transcript.txt', 'w') as f:
            f.write(transcript)
        os.chdir('..')