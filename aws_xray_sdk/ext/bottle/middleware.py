from bottle import request, response, SimpleTemplate

from aws_xray_sdk.core.lambda_launcher import check_in_lambda, LambdaContext
from aws_xray_sdk.core.models import http
from aws_xray_sdk.core.utils import stacktrace
from aws_xray_sdk.ext.util import calculate_sampling_decision, \
    calculate_segment_name, construct_xray_header, prepare_response_header


class XRayMiddleware:
    """
    Middleware that wraps each incoming request to a segment.
    """
    name = 'xray'
    api = 2

    def __init__(self, recorder):
        self._recorder = recorder
        self._in_lambda_ctx = False

        if check_in_lambda() and type(self._recorder.context) == LambdaContext:
            self._in_lambda_ctx = True

        _patch_render(recorder)

    def apply(self, callback, route):
        """
        Apply middleware directly to each route callback.
        """
        pass

def _patch_render(recorder):

    pass
