import wrapt

from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core.models import http
from aws_xray_sdk.ext.util import inject_trace_header, strip_url, get_hostname


def patch():

    wrapt.wrap_function_wrapper(
        'requests',
        'Session.request',
        _xray_traced_requests
    )

    wrapt.wrap_function_wrapper(
        'requests',
        'Session.prepare_request',
        _inject_header
    )


def _xray_traced_requests(wrapped, instance, args, kwargs):

    pass


def _inject_header(wrapped, instance, args, kwargs):
    pass


def requests_processor(wrapped, instance, args, kwargs,
                       return_value, exception, subsegment, stack):

    pass
