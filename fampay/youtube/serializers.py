# Third Party Stuff
from rest_framework import serializers

from .constants import ThumbnailTypes
from .models import YTChannel, YTThumbnail, YTVideo

THUMBNAIL_REVERSE_MAPPINGS = ThumbnailTypes.reverse_mappings()


class YTThumbnailSerializer(serializers.ModelSerializer):
    """
    Serializes the Thumbnail data
    """

    thumbnail_type = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = YTThumbnail
        fields = [
            "thumbnail_url",
            "thumbnail_width",
            "thumbnail_height",
            "thumbnail_type",
        ]

    def get_thumbnail_type(self, obj) -> str:
        """Convert thumbnail_type to actual thumbnail type
        Eg:
        0 -> default
        Args:
            obj: Thumbnail obj
        Returns:
            str: Thumbnail Type
        """
        return THUMBNAIL_REVERSE_MAPPINGS.get(obj.thumbnail_type, "")


class YTChannelSerializer(serializers.ModelSerializer):
    """
    Serializes the Youtube Channel data
    """

    class Meta:
        model = YTChannel
        fields = ["channel_id", "channel_title"]


class YTVideoSerializer(serializers.ModelSerializer):
    """
    Serializes the Youtube Video data
    """

    video_channel = YTChannelSerializer(many=False, read_only=True)
    thumbnails = YTThumbnailSerializer(many=True, read_only=True)

    class Meta:
        model = YTVideo
        fields = "__all__"


class SearchQuerySerializer(serializers.Serializer):
    """
    Used for search query
    """

    search_query = serializers.CharField(
        required=True, allow_null=False, allow_blank=False
    )
