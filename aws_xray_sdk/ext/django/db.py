import copy
import logging
import importlib

from django.db import connections

from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.dbapi2 import XRayTracedCursor

log = logging.getLogger(__name__)


def patch_db():
    for conn in connections.all():
        module = importlib.import_module(conn.__module__)
        _patch_conn(getattr(module, conn.__class__.__name__))


class DjangoXRayTracedCursor(XRayTracedCursor):
    def execute(self, query, *args, **kwargs):
        pass

    def executemany(self, query, *args, **kwargs):
        pass

    def callproc(self, proc, args):
        pass


def _patch_cursor(cursor_name, conn):
    attr = '_xray_original_{}'.format(cursor_name)

    if hasattr(conn, attr):
        log.debug('django built-in db {} already patched'.format(cursor_name))
        return

    if not hasattr(conn, cursor_name):
        log.debug('django built-in db does not have {}'.format(cursor_name))
        return

    setattr(conn, attr, getattr(conn, cursor_name))

    meta = {}

    if hasattr(conn, 'vendor'):
        meta['database_type'] = conn.vendor

    def cursor(self, *args, **kwargs):

        pass

    setattr(conn, cursor_name, cursor)


def _patch_conn(conn):
    _patch_cursor('cursor', conn)
    _patch_cursor('chunked_cursor', conn)
