# Standard Library
from datetime import datetime
from typing import Any, Dict, List

# Third Party Stuff
from dateutil.parser import parse
from django.contrib.postgres.search import SearchQuery, SearchVector
from django.db.models import QuerySet

from .constants import ThumbnailTypes
from .models import YTChannel, YTThumbnail, YTVideo

THUMBNAIL_TYPES = ThumbnailTypes.mappings()


def insert_yt_channel(channel_id: str, channel_title: str) -> YTChannel:
    """Inserts YT channel if not exists
    Args:
        channel_id(str): Channel ID (Primary Key)
        channel_title(str): Channel Title
    Returns:
        YTChannel object
    """
    channel, _ = YTChannel.objects.get_or_create(
        channel_id=channel_id,
        defaults={"channel_id": channel_id, "channel_title": channel_title},
    )
    return channel


def insert_thumbnails(thumbnails: List[Dict[str, Any]], yt_video: YTVideo):
    """Inserts YT Video thumbnails
    Args:
        thumbnails(List): Thumbnail info to be inserted
        yt_video(YTVideo): Video to which thumbnail belongs
    """
    thumbnail_entries = [
        YTThumbnail(**thumbnail, thumbnail_video=yt_video) for thumbnail in thumbnails
    ]
    _ = YTThumbnail.objects.bulk_create(thumbnail_entries)


def insert_yt_video(
    id: str,
    title: str,
    description: str,
    published_at: datetime,
    etag: str,
    channel_info: Dict,
    thumbnails: List[Dict[str, Any]],
) -> YTVideo:
    """Inserts YT Video
    1. Get YT channel (create if not exists)
    2. Create Video
    3. Insert Thumbnails if video is newly created
    Args:
        id(str): Video Id
        title(str): Video title
        description(str): Video Description
        published_at(datetime): Video published datetime
        etag(str): Video etag
        channel_info(Dict): Channel information
        thumbnails(List): List of thumbnails
    Returns:
        Video object
    """
    channel = insert_yt_channel(**channel_info)
    video, created = YTVideo.objects.get_or_create(
        video_id=id,
        defaults={
            "video_id": id,
            "video_title": title,
            "video_description": description,
            "video_published_at": published_at,
            "video_etag": etag,
            "video_channel": channel,
        },
    )
    if created:
        insert_thumbnails(thumbnails, video)
    return video


def process_yt_video_data(video_data: Dict):
    """Extras Video information like video meta info, channel info and thumbnails info
    and inserts into database
    Args:
        video_data(Dict): contains raw data
    Raises:
        Exception: If insertion or processing of meta info fails
    """
    try:
        video_id = video_data["id"]["videoId"]
        video_etag = video_data["etag"]
        video_title = video_data["snippet"]["title"]
        video_description = video_data["snippet"]["description"]
        video_published_at = parse(video_data["snippet"]["publishedAt"])
        thumbnails_data = video_data["snippet"]["thumbnails"]
        thumbnails = [
            {
                "thumbnail_type": THUMBNAIL_TYPES.get(k, 0),
                "thumbnail_url": v["url"],
                "thumbnail_width": v["width"],
                "thumbnail_height": v["height"],
            }
            for k, v in thumbnails_data.items()
        ]
        channel_info = {
            "channel_id": video_data["snippet"]["channelId"],
            "channel_title": video_data["snippet"]["channelTitle"],
        }
        _ = insert_yt_video(
            video_id,
            video_title,
            video_description,
            video_published_at,
            video_etag,
            channel_info,
            thumbnails,
        )
    except Exception as e:
        raise Exception(e)


def search_videos(search_query: str) -> QuerySet[YTVideo]:
    """Search video using the full text search on title and description
    Args:
        search_query(str): search query
    Returns:
        List of filters videos on basis of the search query
    """
    query = SearchQuery(search_query, search_type="raw")
    data = (
        YTVideo.objects.select_related("video_channel")
        .prefetch_related("thumbnails")
        .annotate(search=SearchVector("video_title", "video_description"))
        .filter(search=query)
    )
    return data
