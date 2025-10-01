import os

from dotenv import load_dotenv

from db import _ensure_csv_exists, insert_line
from youtube_client import YoutubeClient


def main():
    load_dotenv()

    API_VERSION = os.getenv("API_VERSION")
    API_KEY = os.getenv("YOUTUBE_DATA_API_KEY")
    CHANNEL_ID = os.getenv("CHANNEL_ID")

    ROOT_DIR = os.path.dirname(__file__)
    CHANNEL_CSV_PATH = os.path.join(ROOT_DIR, "channel.csv")
    VIDEO_CSV_PATH = os.path.join(ROOT_DIR, "video.csv")

    client = YoutubeClient(API_KEY, API_VERSION)
    channel = client.get_channel_info(CHANNEL_ID)
    videos = client.get_recent_videos_from_channel(channel.uploads_playlist_id)

    _ensure_csv_exists(CHANNEL_CSV_PATH, list(channel.__dict__().keys()))
    _ensure_csv_exists(VIDEO_CSV_PATH, list(videos[0].__dict__().keys()))

    insert_line(CHANNEL_CSV_PATH, channel)
    for v in videos:
        insert_line(VIDEO_CSV_PATH, v)


if __name__ == "__main__":
    main()
