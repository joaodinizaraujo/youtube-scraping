import os
from datetime import datetime

import psycopg2
from psycopg2._psycopg import connection

from youtube_client import Channel, Video


def _get_conn() -> connection:
    return psycopg2.connect(
        database=os.getenv("POSTGRESQL_DBNAME"),
        user=os.getenv("POSTGRESQL_USER"),
        password=os.getenv("POSTGRESQL_PASSWORD"),
        host=os.getenv("POSTGRESQL_HOST"),
        port=os.getenv("POSTGRESQL_PORT")
    )


def _close(conn) -> None:
    conn.cursor().close()
    conn.close()


def insert_channel(c: Channel) -> None:
    conn = _get_conn()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO channel (
            picture_date, 
            channel_id, 
            name, 
            views, 
            subscribers_count, 
            video_count,
            uploads_playlist_id
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        (
            datetime.now(),
            c.channel_id,
            c.name,
            c.views,
            c.subscribers_count,
            c.video_count,
            c.uploads_playlist_id
        )
    )

    conn.commit()

    _close(conn)


def insert_video(v: Video) -> None:
    conn = _get_conn()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO video (
            picture_date, 
            video_id, 
            channel_id, 
            title, 
            published_at, 
            views, 
            like_count, 
            comment_count
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            datetime.now(),
            v.video_id,
            v.channel_id,
            v.title,
            v.published_at,
            v.views,
            v.like_count,
            v.comment_count
        )
    )

    conn.commit()

    _close(conn)
