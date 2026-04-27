import flask.templating
from flask import request

from aws_xray_sdk.core.models import http
from aws_xray_sdk.core.utils import stacktrace
from aws_xray_sdk.ext.util import calculate_sampling_decision, \
    calculate_segment_name, construct_xray_header, prepare_response_header
from aws_xray_sdk.core.lambda_launcher import check_in_lambda, LambdaContext


class XRayMiddleware:

    def __init__(self, app, recorder):
        self.app = app
        self.app.logger.info("initializing xray middleware")

        self._recorder = recorder
        self.app.before_request(self._before_request)
        self.app.after_request(self._after_request)
        self.app.teardown_request(self._teardown_request)
        self.in_lambda_ctx = False

        if check_in_lambda() and type(self._recorder.context) == LambdaContext:
            self.in_lambda_ctx = True

        _patch_render(recorder)

    def _before_request(self):
        pass

    def _after_request(self, response):
        pass

    def _teardown_request(self, exception):
        pass


def _patch_render(recorder):

    pass
