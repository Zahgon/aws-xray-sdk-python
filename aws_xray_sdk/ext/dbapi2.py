import copy
import wrapt

from aws_xray_sdk.core import xray_recorder


class XRayTracedConn(wrapt.ObjectProxy):

    _xray_meta = None

    def __init__(self, conn, meta={}):

        super().__init__(conn)
        self._xray_meta = meta

    def cursor(self, *args, **kwargs):

        pass


class XRayTracedCursor(wrapt.ObjectProxy):

    _xray_meta = None

    def __init__(self, cursor, meta={}):

        super().__init__(cursor)
        self._xray_meta = meta

        # we preset database type if db is framework built-in
        if not self._xray_meta.get('database_type'):
            db_type = cursor.__class__.__module__.split('.')[0]
            self._xray_meta['database_type'] = db_type

    def __enter__(self):

        value = self.__wrapped__.__enter__()
        if value is not self.__wrapped__:
            return value
        return self

    @xray_recorder.capture()
    def execute(self, query, *args, **kwargs):

        pass

    @xray_recorder.capture()
    def executemany(self, query, *args, **kwargs):

        pass

    @xray_recorder.capture()
    def callproc(self, proc, args):

        pass


def add_sql_meta(meta):

    pass
