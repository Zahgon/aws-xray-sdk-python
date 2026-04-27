import logging
import sys
from urllib.parse import urlparse, uses_netloc, quote_plus

import wrapt
from sqlalchemy.sql.expression import ClauseElement

from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core.patcher import _PATCHED_MODULES
from aws_xray_sdk.core.utils import stacktrace
from aws_xray_sdk.ext.util import unwrap


def _sql_meta(engine_instance, args):
    pass


def _xray_traced_sqlalchemy_execute(wrapped, instance, args, kwargs):
    pass


def _xray_traced_sqlalchemy_session(wrapped, instance, args, kwargs):
    pass


def _process_request(wrapped, engine_instance, args, kwargs):
    pass


def patch():
    wrapt.wrap_function_wrapper(
        'sqlalchemy.engine.base',
        'Connection.execute',
        _xray_traced_sqlalchemy_execute
    )

    wrapt.wrap_function_wrapper(
        'sqlalchemy.orm.session',
        'Session.execute',
        _xray_traced_sqlalchemy_session
    )


def unpatch():
    """
    Unpatch any previously patched modules.
    This operation is idempotent.
    """
    _PATCHED_MODULES.discard('sqlalchemy_core')
    import sqlalchemy
    unwrap(sqlalchemy.engine.base.Connection, 'execute')
    unwrap(sqlalchemy.orm.session.Session, 'execute')
