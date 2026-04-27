import copy
import re
import wrapt
from operator import methodcaller

from aws_xray_sdk.ext.dbapi2 import XRayTracedConn, XRayTracedCursor


def patch():
    wrapt.wrap_function_wrapper(
        'psycopg2',
        'connect',
        _xray_traced_connect
    )
    wrapt.wrap_function_wrapper(
        'psycopg2.extensions',
        'register_type',
        _xray_register_type_fix
    )
    wrapt.wrap_function_wrapper(
        'psycopg2.extensions',
        'quote_ident',
        _xray_register_type_fix
    )

    wrapt.wrap_function_wrapper(
        'psycopg2.extras',
        'register_default_jsonb',
        _xray_register_default_jsonb_fix
    )


def _xray_traced_connect(wrapped, instance, args, kwargs):
    pass


def _xray_register_type_fix(wrapped, instance, args, kwargs):
    """Send the actual connection or curser to register type."""
    pass


def _xray_register_default_jsonb_fix(wrapped, instance, args, kwargs):
    pass
