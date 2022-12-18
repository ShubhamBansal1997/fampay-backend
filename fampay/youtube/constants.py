# Standard Library
from enum import IntEnum


class ThumbnailTypes(IntEnum):
    """
    Thumbnail Types

    ...
    Attributes
    ----------

    Methods
    ----------
    choices(self):
        Gives list of tuple with enum key value pairs
    """

    DEFAULT = 0
    MEDIUM = 1
    HIGH = 2
    STANDARD = 3
    MAXRES = 4

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

    @classmethod
    def mappings(cls):
        return {key.name.lower(): key.value for key in cls}

    @classmethod
    def reverse_mappings(cls):
        return {key.value: key.name.lower() for key in cls}


YT_SEARCH_API = "https://www.googleapis.com/youtube/v3/search"
YT_API_REDIS_KEY = "fam_pay:youtube:yt_api_redis_key"
YT_API_NEXT_PAGE_TOKEN = "fam_pay:youtube:yt_api_next_page_token"
YT_API_PUBLISHED_AT = "fam_pay:youtube:yt_api_published_at"

DEFAULT_API_ERROR = "API Error"
QUOTA_API_ERROR = "quotaExceeded"
