# Third Party Stuff
from rest_framework.renderers import JSONRenderer


class FampayApiRenderer(JSONRenderer):
    media_type = "application/vnd.fampay+json"
