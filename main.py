import os

from dotenv import load_dotenv

from youtube_client import YoutubeClient


def main():
    load_dotenv()

    API_VERSION = os.getenv("API_VERSION")
    API_KEY = os.getenv("YOUTUBE_DATA_API_KEY")
    CHANNEL_ID = os.getenv("CHANNEL_ID")

    client = YoutubeClient(API_KEY, API_VERSION)
    channel = client.get_channel_info(CHANNEL_ID)
    videos = client.get_recent_videos_from_channel(channel.uploads_playlist_id)


if __name__ == "__main__":
    main()
