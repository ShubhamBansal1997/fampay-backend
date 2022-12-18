# Standard Library
from datetime import datetime, time, timezone
from typing import Dict

# Third Party Stuff
from celery import shared_task
from django.core.cache import cache

# fampay Stuff
from settings.common import YT_SEARCH_TERM

from .constants import QUOTA_API_ERROR, YT_API_NEXT_PAGE_TOKEN, YT_API_PUBLISHED_AT
from .services import process_yt_video_data
from .utils import fetch_yt_video, get_yt_api_key


@shared_task
def yt_video_processing_task(video_data: Dict):
    """Task to process videos from the scheduler
    Args:
        video_data(Dict): Raw video data from the API
    """
    process_yt_video_data(video_data)


@shared_task
def yt_video_scheduler():
    """Scheduler to fetch youtube video at fixed interval
    Note:
        1. Published date is set to today start of the day if not present in the cache
        2. On every Failed API call (due to Quota issue) API resets itself
        3. Next Page token and published at is stored in cache to fetch data till end
        4. Fetched Videos are sent for processing in the yt_video_processing_task
    #TODO
        Added a proper handler in case of failures
    """
    search_term = YT_SEARCH_TERM
    published_date = (
        datetime.combine(datetime.now(), time.min)
        .replace(tzinfo=timezone.utc)
        .isoformat()
        .replace("+00:00", "Z")
    )
    yt_api_key = get_yt_api_key()
    next_page_token = cache.get(YT_API_NEXT_PAGE_TOKEN)
    published_date = cache.get_or_set(YT_API_PUBLISHED_AT, published_date)
    status, data = fetch_yt_video(
        yt_api_key,
        published_after=published_date,
        q=search_term,
        page_token=next_page_token,
    )
    if not status or data == QUOTA_API_ERROR:
        yt_api_key = get_yt_api_key(True)
    else:
        next_page_token = data.get("nextPageToken", None)
        if next_page_token:
            cache.set(YT_API_NEXT_PAGE_TOKEN, next_page_token)
        else:
            cache.delete([YT_API_NEXT_PAGE_TOKEN, YT_API_PUBLISHED_AT])
        for item in data.get("items", []):
            yt_video_processing_task.apply_async(args=(item,), ignore_result=True)
