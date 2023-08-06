import io
import json

from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

import drf_buzz

import requests

from . import serializers


class TestViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = serializers.TestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response()

    @action(detail=False, methods=["post"])
    def buzz(self, request, *args, **kwargs):
        raise drf_buzz.DRFBuzz("basic error")

    @action(detail=False, methods=["post"])
    def exception(self, request, *args, **kwargs):
        raise Exception("exception error")

    @action(detail=False, methods=["post"])
    def requests(self, request, *args, **kwargs):
        r = requests.Response()
        r.url = "some url"
        reason = u"Komponenttia ei löydy"
        r.reason = reason.encode("latin-1")
        r.raw = io.BytesIO(json.dumps({"code": "InvalidToken", "description": "Invalid token."}).encode())
        r.status_code = 400
        r.encoding = None
        r.raise_for_status()
