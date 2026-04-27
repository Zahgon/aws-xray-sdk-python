import pg8000
import wrapt

from aws_xray_sdk.ext.dbapi2 import XRayTracedConn
from aws_xray_sdk.core.patcher import _PATCHED_MODULES
from aws_xray_sdk.ext.util import unwrap


def patch():

    wrapt.wrap_function_wrapper(
        'pg8000',
        'connect',
        _xray_traced_connect
    )


def _xray_traced_connect(wrapped, instance, args, kwargs):

    pass


def unpatch():
    """
    Unpatch any previously patched modules.
    This operation is idempotent.
    """
    _PATCHED_MODULES.discard('pg8000')
    unwrap(pg8000, 'connect')
