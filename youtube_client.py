from datetime import timedelta, datetime
from typing import Optional

from googleapiclient.discovery import build


class Channel:
    def __init__(
        self,
        channel_id: str,
        name: str,
        views: int,
        subscribers_count: int,
        video_count: int,
        uploads_playlist_id: str
    ):
        self.channel_id = channel_id
        self.name = name
        self.views = views
        self.subscribers_count = subscribers_count
        self.video_count = video_count
        self.uploads_playlist_id = uploads_playlist_id


class Video:
    def __init__(
        self,
        video_id: str,
        channel_id: str,
        title: str,
        published_at: datetime,
        views: Optional[int] = None,
        like_count: Optional[int] = None,
        comment_count: Optional[int] = None
    ):
        self.video_id = video_id
        self.channel_id = channel_id
        self.title = title
        self.views = views
        self.published_at = published_at
        self.like_count = like_count
        self.comment_count = comment_count


class YoutubeClient:
    def __init__(
        self,
        api_key: str,
        api_version: str = "v3"
    ):
        self.youtube = build("youtube", api_version, developerKey=api_key)

    def get_channel_info(self, channel_id: str) -> Channel:
        request = self.youtube.channels().list(
            part="statistics,snippet,contentDetails",
            id=channel_id
        )
        response = request.execute()

        return Channel(
            channel_id=channel_id,
            name=response["items"][0]["snippet"]["title"],
            views=int(response["items"][0]["statistics"]["viewCount"]),
            subscribers_count=int(response["items"][0]["statistics"]["subscriberCount"]),
            video_count=int(response["items"][0]["statistics"]["videoCount"]),
            uploads_playlist_id=response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
        )

    def get_recent_videos_from_channel(
        self,
        uploads_playlist_id: str,
        published_after: datetime = datetime.now() - timedelta(weeks=3)
    ) -> list[Video]:
        request = self.youtube.playlistItems().list(
            part="snippet",
            playlistId=uploads_playlist_id
        )
        response = request.execute()

        videos = []
        while True:
            published_at = None
            for i in response["items"]:
                published_at = datetime.fromisoformat(
                    i["snippet"]["publishedAt"].replace('Z', '+00:00')
                )
                if published_at.replace(tzinfo=None) < published_after:
                    break

                videos.append(Video(
                    video_id=i["snippet"]["resourceId"]["videoId"],
                    channel_id=i["snippet"]["channelId"],
                    title=i["snippet"]["title"],
                    published_at=published_at
                ))
            else:
                request = self.youtube.playlistItems().list_next(request, response)
                if request is None:
                    break

                response = request.execute()

            if published_at is None or published_at.replace(tzinfo=None) < published_after:
                break

        for video in videos:
            request = self.youtube.videos().list(
                part="statistics",
                id=video.video_id
            )
            response = request.execute()

            video.like_count = int(response["items"][0]["statistics"]["likeCount"])
            video.comment_count = int(response["items"][0]["statistics"]["commentCount"])
            video.views = int(response["items"][0]["statistics"]["viewCount"])

        return videos
