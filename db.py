import csv
import os
from datetime import datetime

from youtube_client import Channel, Video


def _ensure_csv_exists(csv_path: str, headers: list) -> None:
    if not os.path.exists(csv_path):
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter="|")
            writer.writerow(headers + ["picture_date"])


def insert_line(csv_path: str, r: Channel | Video) -> None:
    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter="|")
        writer.writerow(list(r.__dict__().values()) + [str(datetime.now().date())])
