# Standard Library
from typing import Dict, Optional, Union

# Third Party Stuff
import requests
from django.core.cache import cache

# fampay Stuff
from settings.common import YT_API_KEYS

from .constants import YT_API_REDIS_KEY, YT_SEARCH_API


def get_yt_api_key(failed: bool = False) -> str:
    """Get YT API Key
    1. Get the Current API key from the cache if present
    2. If the API fails it will pick the next API key
    Args:
        failed(bool): To get the next working API key
    Returns:
        Return the YT API key
    """
    yt_api_key = cache.get(YT_API_REDIS_KEY)
    if yt_api_key and not failed:
        return yt_api_key
    try:
        next_yt_next_key_pos = YT_API_KEYS.index(yt_api_key) + 1
        yt_api_key = YT_API_KEYS[next_yt_next_key_pos]
    except ValueError:
        yt_api_key = YT_API_KEYS[0]
    except IndexError:
        yt_api_key = YT_API_KEYS[0]
    finally:
        cache.set(YT_API_REDIS_KEY, yt_api_key)
    return yt_api_key


def fetch_yt_video(
    yt_api_key: str,
    published_after: str,
    part: str = "snippet",
    q: str = "cricket",
    type: str = "video",
    order: str = "date",
    page_token: Optional[str] = None,
):
    """Call YT API to fetch the Video
    Args:
        yt_api_key(str): YT API Key
        published_at(str): Date time after which you want to fetch the videos
        part(str): includes meta info
        q(str): Search term
        type(str): Type of search
        order(str): Order of the videos
        page_token(str): Page token to jump to next page
    """
    payload: Dict[str, Union[int, str]] = {
        "part": part,
        "q": q,
        "type": type,
        "order": order,
        "publishedAfter": published_after,
        "maxResults": 50,
        "key": yt_api_key,
    }
    if page_token:
        payload["pageToken"] = page_token
    response = requests.get(YT_SEARCH_API, params=payload)
    data = response.json()
    if response.status_code == 200:
        return True, data
    else:
        errors = data.get("error", {}).get("errors", [])
        if len(errors):
            return False, errors[0]
        return False, data
