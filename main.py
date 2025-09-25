import os

from dotenv import load_dotenv
from googleapiclient.discovery import build


def main():
    load_dotenv()

    api_service_name = "youtube"
    api_version = "v3"

    api_key = os.getenv("YOUTUBE_DATA_API_KEY")

    youtube = build(api_service_name, api_version, developerKey=api_key)

    request = youtube.channels().list(
        part="statistics",
        id="UCbcqRrT5zquRLfrRqI90yFw"
    )
    response = request.execute()

    print(response)


if __name__ == "__main__":
    main()
