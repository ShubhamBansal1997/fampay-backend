# Third Party Stuff
from django.db import models
from django.utils.translation import gettext_lazy as _

# fampay Stuff
from fampay.base.models import TimeStampedModel

from .constants import ThumbnailTypes

# Create your models here.


class YTChannel(TimeStampedModel):
    channel_id = models.CharField(
        _("Channel Id"), max_length=25, null=False, blank=False, primary_key=True
    )
    channel_title = models.CharField(
        _("Channel Title"), max_length=100, null=False, blank=False
    )

    class Meta:
        verbose_name = _("yt_channel")
        verbose_name_plural = _("yt_channels")
        ordering = ("-created_at",)


class YTVideo(TimeStampedModel):
    video_id = models.CharField(
        _("Video Id"), max_length=25, null=False, blank=False, primary_key=True
    )
    video_title = models.CharField(
        _("Video Title"), max_length=250, null=False, blank=False
    )
    video_description = models.TextField(
        _("Channel Description"), null=False, blank=False
    )
    video_published_at = models.DateTimeField(
        _("Channel Published At"), null=False, blank=False
    )
    video_channel = models.ForeignKey(
        YTChannel,
        related_name="channel",
        null=False,
        blank=False,
        on_delete=models.PROTECT,
    )
    video_etag = models.CharField(
        _("Channel Etag"), max_length=50, null=False, blank=False
    )

    class Meta:
        verbose_name = _("yt_video")
        verbose_name_plural = _("yt_videos")
        ordering = ("-video_published_at",)
        indexes = [
            models.Index(
                fields=[
                    "video_title",
                ]
            ),
            models.Index(
                fields=[
                    "video_description",
                ]
            ),
            models.Index(
                fields=[
                    "video_published_at",
                ]
            ),
        ]


class YTThumbnail(TimeStampedModel):
    thumbnail_url = models.CharField(
        _("Thumbnail URL"), max_length=100, null=False, blank=False
    )
    thumbnail_width = models.PositiveSmallIntegerField(
        _("Thumbnail width"), null=False, blank=False
    )
    thumbnail_height = models.PositiveSmallIntegerField(
        _("Thumbnail height"), null=False, blank=False
    )
    thumbnail_type = models.PositiveBigIntegerField(
        _("Thumbnail type"), null=False, blank=False, choices=ThumbnailTypes.choices()
    )
    thumbnail_video = models.ForeignKey(
        YTVideo,
        related_name="thumbnails",
        null=False,
        blank=False,
        on_delete=models.PROTECT,
    )

    class Meta:
        verbose_name = _("yt_thumbnail")
        verbose_name_plural = _("yt_thumbnails")
        ordering = ("-created_at",)
        constraints = [
            models.UniqueConstraint(
                fields=["thumbnail_video", "thumbnail_type", "thumbnail_url"],
                name="yt_thumbnail_primary_keys",
            )
        ]
