import wrapt
from operator import methodcaller

from aws_xray_sdk.ext.dbapi2 import XRayTracedConn


def patch():
    wrapt.wrap_function_wrapper(
        'psycopg',
        'connect',
        _xray_traced_connect
    )

    wrapt.wrap_function_wrapper(
        'psycopg_pool.pool',
        'ConnectionPool._connect',
        _xray_traced_connect
    )


def _xray_traced_connect(wrapped, instance, args, kwargs):
    pass
