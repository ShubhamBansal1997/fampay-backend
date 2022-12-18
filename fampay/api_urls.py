# Third Party Stuff
from rest_framework.routers import DefaultRouter

# fampay Stuff
from fampay.base.api.routers import SingletonRouter
from fampay.users.api import CurrentUserViewSet
from fampay.users.auth.api import AuthViewSet
from fampay.youtube.api import YTVideoViewSet

default_router = DefaultRouter(trailing_slash=False)
singleton_router = SingletonRouter(trailing_slash=False)

# Register all the django rest framework viewsets below.
default_router.register("auth", AuthViewSet, basename="auth")
singleton_router.register("me", CurrentUserViewSet, basename="me")
default_router.register("video", YTVideoViewSet, basename="video")

# Combine urls from both default and singleton routers and expose as
# 'urlpatterns' which django can pick up from this module.
urlpatterns = default_router.urls + singleton_router.urls
