from pytube import YouTube

#where to save
SAVE_PATH = "./video/"  #to_do

youtube_urls = [
  "https://www.youtube.com/watch?v=sZDpJHl6amo",
  "https://www.youtube.com/shorts/vbXfyNxnkcs",
  "https://www.youtube.com/watch?v=AvsIogVNs7w",
  "https://www.youtube.com/shorts/xq3aFCEnFrQ",
  "https://www.youtube.com/shorts/IhvEU-6bnrM",
  "https://www.youtube.com/watch?v=SvHpy_tk9DQ",
  "https://www.youtube.com/watch?v=zFDz4zmM990",
  "https://www.youtube.com/watch?v=m_H4zguqeRM",
  "https://www.youtube.com/watch?v=RwcV4DJUEvM",
  "https://www.youtube.com/watch?v=E5d-qNAuArs",
  "https://www.youtube.com/watch?v=Lq_xbt1cqg4",
  "https://www.youtube.com/watch?v=gPZA98whQGI",
]

for i in youtube_urls:
  try:
    yt = YouTube(i)
  except:
    print("Connection Error")
  try:
    name = yt.author.lower().replace(" ", "") + '.mp4'
    yt.streams.filter(progressive=True,file_extension='mp4').order_by('resolution')[-1].download(SAVE_PATH,filename=name)
    print("Downloaded " + name)
  except:
    print("Some Error!")
print('Task Completed!')
