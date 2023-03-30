"""
This module downloads videos from YouTube.
Author: bonsaiskyline
"""
import os
from pytube import YouTube

VIDEO_DIR = "../video/"

YOUTUBE_URLS = [
    # "https://www.youtube.com/watch?v=sZDpJHl6amo",
    # "https://www.youtube.com/shorts/vbXfyNxnkcs",
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


def download_youtube_videos(
    youtube_urls: list,
    save_path: str
):
    """
    Downloads videos.

    Args:
      youtube_urls (list): List of YouTube URLs.
      save_path (str): Path to save videos.
    """
    for url in youtube_urls:
        try:
            youtube = YouTube(url)
            name = youtube.author.lower().replace(" ", "") + '.mp4'
            if not os.path.isfile(save_path + name):
                filtered_streams = youtube.streams.filter(
                    progressive=True,
                    file_extension='mp4'
                )
                ordered_streams = filtered_streams.order_by(
                    'resolution'
                )[-1]
                ordered_streams.download(
                    save_path,
                    filename=name
                )
                print("Downloaded " + name)
        except Exception as exception:
            print("An error occurred:", exception)
            print('Task Completed!')


if __name__ == "__main__":
    download_youtube_videos(
        youtube_urls=YOUTUBE_URLS,
        save_path=VIDEO_DIR
    )
