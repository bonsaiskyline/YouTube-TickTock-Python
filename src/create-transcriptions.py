
import os
from .notebook-transcribe import group

os.chdir('temp')
current = os.getcwd()
for folder_name in os.listdir(current):
    folder_path = os.path.join(current, folder_name)
    if os.path.isdir(folder_path):
        print(f"Folder found: {folder_name}")
        output_file = "diarization.txt"
        groups = group(output_file)


# for g in groups:
#     shift = re.findall('[0-9]+:[0-9]+:[0-9]+\.[0-9]+', string=g[0])[0]
#     shift = millisec(shift) - SPACERMILLI #the start time in the original video
#     shift=max(shift, 0)
#     gidx += 1
#     captions = json.load(open(str(gidx) + '.json'))['segments']

#     if captions:
#         speaker = g[0].split()[-1]
#         boxclr = def_boxclr
#         spkrclr = def_spkrclr
#         if speaker in speakers:
#             speaker, boxclr, spkrclr = speakers[speaker]

#         html.append(f'<div class="e" style="background-color: {boxclr}">\n');
#         html.append('<p  style="margin:0;padding: 5px 10px 10px 10px;word-wrap:normal;white-space:normal;">\n')
#         html.append(f'<span style="color:{spkrclr};font-weight: bold;">{speaker}</span><br>\n\t\t\t\t')

#         for c in captions:
#             start = shift + c['start'] * 1000.0
#             start = start / 1000.0   #time resolution ot youtube is Second.
#             end = (shift + c['end'] * 1000.0) / 1000.0
#             txt.append(f'[{timeStr(start)} --> {timeStr(end)}] [{speaker}] {c["text"]}\n')

#             for i, w in enumerate(c['words']):
#                 if w == "":
#                     continue
#                 start = (shift + w['start']*1000.0) / 1000.0
#                 #end = (shift + w['end']) / 1000.0   #time resolution ot youtube is Second.
#                 html.append(f'<a href="#{timeStr(start)}" id="{"{:.1f}".format(round(start*5)/5)}" class="lt" onclick="jumptoTime({int(start)}, this.id)">{w["word"]}</a><!--\n\t\t\t\t-->')
#             #html.append('\n')
#         html.append('</p>\n')
#         html.append(f'</div>\n')
