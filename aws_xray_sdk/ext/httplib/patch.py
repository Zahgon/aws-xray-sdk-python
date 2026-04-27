import fnmatch
from collections import namedtuple

import urllib3.connection
import wrapt

from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core.exceptions.exceptions import SegmentNotFoundException
from aws_xray_sdk.core.models import http
from aws_xray_sdk.core.patcher import _PATCHED_MODULES
from aws_xray_sdk.ext.util import get_hostname, inject_trace_header, strip_url, unwrap

httplib_client_module = 'http.client'
import http.client as httplib

_XRAY_PROP = '_xray_prop'
_XRay_Data = namedtuple('xray_data', ['method', 'host', 'url'])
_XRay_Ignore = namedtuple('xray_ignore', ['subclass', 'hostname', 'urls'])
# A flag indicates whether this module is X-Ray patched or not
PATCH_FLAG = '__xray_patched'
# Calls that should be ignored
_XRAY_IGNORE = set()


def add_ignored(subclass=None, hostname=None, urls=None):
    global _XRAY_IGNORE
    if subclass is not None or hostname is not None or urls is not None:
        urls = urls if urls is None else tuple(urls)
        _XRAY_IGNORE.add(_XRay_Ignore(subclass=subclass, hostname=hostname, urls=urls))


def reset_ignored():
    global _XRAY_IGNORE
    _XRAY_IGNORE.clear()
    _ignored_add_default()


def _ignored_add_default():
    # skip httplib tracing for SDK built-in centralized sampling pollers
    add_ignored(subclass='botocore.awsrequest.AWSHTTPConnection', urls=['/GetSamplingRules', '/SamplingTargets'])


# make sure we have the default rules
_ignored_add_default()


def http_response_processor(wrapped, instance, args, kwargs, return_value,
                            exception, subsegment, stack):
    pass


def _xray_traced_http_getresponse(wrapped, instance, args, kwargs):
    pass


def http_send_request_processor(wrapped, instance, args, kwargs, return_value,
                                exception, subsegment, stack):
    pass


def _ignore_request(instance, hostname, url):
    pass


def _send_request(wrapped, instance, args, kwargs):
    pass


def http_read_processor(wrapped, instance, args, kwargs, return_value,
                        exception, subsegment, stack):
    pass


def _xray_traced_http_client_read(wrapped, instance, args, kwargs):
    pass


def patch():
    """
    patch the built-in `urllib/httplib/httplib.client` methods for tracing.
    """
    if getattr(httplib, PATCH_FLAG, False):
        return
    # we set an attribute to avoid multiple wrapping
    setattr(httplib, PATCH_FLAG, True)

    wrapt.wrap_function_wrapper(
        httplib_client_module,
        'HTTPConnection._send_request',
        _send_request
    )

    wrapt.wrap_function_wrapper(
        httplib_client_module,
        'HTTPConnection.getresponse',
        _xray_traced_http_getresponse
    )

    wrapt.wrap_function_wrapper(
        httplib_client_module,
        'HTTPResponse.read',
        _xray_traced_http_client_read
    )


def unpatch():
    """
    Unpatch any previously patched modules.
    This operation is idempotent.
    """
    _PATCHED_MODULES.discard('httplib')
    setattr(httplib, PATCH_FLAG, False)
    # _send_request encapsulates putrequest, putheader[s], and endheaders
    unwrap(httplib.HTTPConnection, '_send_request')
    unwrap(httplib.HTTPConnection, 'getresponse')
    unwrap(httplib.HTTPResponse, 'read')
