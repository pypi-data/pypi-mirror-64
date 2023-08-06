import logging

import buzz
from django.utils.translation import ugettext_lazy as _

import rest_framework.exceptions
from rest_framework.views import exception_handler as base_exception_handler

import requests.exceptions

LOG = logging.getLogger("django")
VERSION = "0.3.1"


def is_pretty(data):
    if "description" in data and "code" in data and isinstance(data, dict) and isinstance(data.get("fields", []), list):
        return True
    return False


class DRFBuzz(buzz.Buzz, rest_framework.exceptions.APIException):
    def __init__(self, message, *format_args, **format_kwds):
        super().__init__(message=message, *format_args, **format_kwds)
        rest_framework.exceptions.APIException.__init__(self=self, detail=message, code=repr(self))


def exception_handler(exc, context):
    # FIXME: implicit requests dependency
    if isinstance(exc, requests.exceptions.HTTPError):
        try:
            response_data = exc.response.json()
        except ValueError:
            pass
        else:
            # Override an exception if it's a pretty enough
            if is_pretty(response_data):
                status_code = exc.response.status_code

                exc = rest_framework.exceptions.APIException(detail=response_data)
                exc.status_code = status_code

    response = base_exception_handler(exc, context)

    # Uncaught exception handling
    if not response:
        LOG.error("Exception occurred", exc_info=exc)

        exc = rest_framework.exceptions.APIException(exc)
        response = base_exception_handler(exc, context)
        response.data["detail"] = _("Internal error")

    if response is not None:
        if is_pretty(response.data):
            return response

        data = {"code": exc.__class__.__name__}

        if "detail" in response.data:
            description = response.data["detail"]
        else:
            description = exc.default_detail
            data["fields"] = response.data

        data["description"] = description

        response.data = data

    return response
