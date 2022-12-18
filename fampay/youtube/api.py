# Third Party Stuff
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

# fampay Stuff
from fampay.base.api.mixins import MultipleSerializerMixin

from .models import YTVideo
from .serializers import SearchQuerySerializer, YTVideoSerializer
from .services import search_videos


class YTVideoViewSet(
    MultipleSerializerMixin, viewsets.GenericViewSet, mixins.ListModelMixin
):
    serializer_class = YTVideoSerializer
    queryset = (
        YTVideo.objects.select_related("video_channel")
        .prefetch_related("thumbnails")
        .all()
    )
    search_fields = ["video_title", "video_description"]
    filter_backends = [OrderingFilter, SearchFilter]
    ordering_fields = ["video_published_at"]
    serializer_classes = {
        "search": SearchQuerySerializer,
    }
    permission_classes = [AllowAny]

    @action(methods=["GET"], detail=False)
    def search(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        data = search_videos(**serializer.validated_data)
        serializer = self.serializer_class(data, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
