import wrapt
import sqlite3

from aws_xray_sdk.ext.dbapi2 import XRayTracedConn


def patch():

    wrapt.wrap_function_wrapper(
        'sqlite3',
        'connect',
        _xray_traced_connect
    )


def _xray_traced_connect(wrapped, instance, args, kwargs):

    pass


class XRayTracedSQLite(XRayTracedConn):

    def execute(self, *args, **kwargs):
        pass

    def executemany(self, *args, **kwargs):
        pass
