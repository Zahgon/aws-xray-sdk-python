import json
import wrapt
import pynamodb

from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core.models import http
from aws_xray_sdk.ext.boto_utils import _extract_whitelisted_params

PYNAMODB4 = int(pynamodb.__version__.split('.')[0]) >= 4

if PYNAMODB4:
    import botocore.httpsession
else:
    import botocore.vendored.requests.sessions


def patch():
    """Patch PynamoDB so it generates subsegements when calling DynamoDB."""

    if PYNAMODB4:
        if hasattr(botocore.httpsession, '_xray_enabled'):
            return
        setattr(botocore.httpsession, '_xray_enabled', True)

        module = 'botocore.httpsession'
        name = 'URLLib3Session.send'
    else:
        if hasattr(botocore.vendored.requests.sessions, '_xray_enabled'):
            return
        setattr(botocore.vendored.requests.sessions, '_xray_enabled', True)

        module = 'botocore.vendored.requests.sessions'
        name = 'Session.send'

    wrapt.wrap_function_wrapper(
        module, name, _xray_traced_pynamodb,
    )


def _xray_traced_pynamodb(wrapped, instance, args, kwargs):

    # Check if it's a request to DynamoDB and return otherwise.
    pass


def pynamodb_meta_processor(wrapped, instance, args, kwargs, return_value,
                            exception, subsegment, stack):
    pass
