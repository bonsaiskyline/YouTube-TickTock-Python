
import os
import re
import json
from util.transcript_utils import group, millisec, SPACERMILLI
from moviepy.editor import VideoFileClip, concatenate_videoclips

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


def merge(mapping, items):
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


mapping = create_mapping()
print("=====================================")
a = " Oh tick tock CEO goes under oath and says his company is not a glaring risk to U.S. national security. Lawmakers though in both parties clearly not convinced. Piercing questions today up on Capitol Hill the hearing in the House Energy and Commerce Committee kicking off with a reminder that misleading Congress is a federal crime. Tick tocks chief very very careful in his answers. He says the app can keep data for millions of American users off limits from the Chinese government. But lawmakers counter. They say simply they don't believe it. They see tick tock as a weapon for the Chinese regime."
b = "Hello there. We begin in the United States where time is ticking for TikTok. The chief of the social media app, Shozy Chu, was grilled by lawmakers over a whole range of issues, mostly related to the company's Chinese ownership. His appearance before the Congressional Committee comes after the Biden administration threatened to ban the social media app if the company's Chinese owners didn't sell their shares. TikTok is wildly popular in the States. It's got over 150 million American users, including almost 5 million businesses. Well, our North America business correspondent, Michelle Flurry, has been following the story from Washington, D.C."
merge(mapping, [mapping[a.strip()], mapping[b.strip()]])