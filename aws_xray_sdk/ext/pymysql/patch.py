import pymysql
import wrapt

from aws_xray_sdk.ext.dbapi2 import XRayTracedConn
from aws_xray_sdk.core.patcher import _PATCHED_MODULES
from aws_xray_sdk.ext.util import unwrap


def patch():

    wrapt.wrap_function_wrapper(
        'pymysql',
        'connect',
        _xray_traced_connect
    )

    # patch alias
    if hasattr(pymysql, 'Connect'):
        pymysql.Connect = pymysql.connect


def _xray_traced_connect(wrapped, instance, args, kwargs):

    pass


def sanitize_db_ver(raw):

    pass


def unpatch():
    """
    Unpatch any previously patched modules.
    This operation is idempotent.
    """
    _PATCHED_MODULES.discard('pymysql')
    unwrap(pymysql, 'connect')
