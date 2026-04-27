import wrapt
import mysql.connector

from aws_xray_sdk.ext.dbapi2 import XRayTracedConn


MYSQL_ATTR = {
    '_host': 'name',
    '_user': 'user',
}


def patch():

    wrapt.wrap_function_wrapper(
        'mysql.connector',
        'connect',
        _xray_traced_connect
    )

    # patch alias
    if hasattr(mysql.connector, 'Connect'):
        mysql.connector.Connect = mysql.connector.connect


def _xray_traced_connect(wrapped, instance, args, kwargs):

    pass


def sanitize_db_ver(raw):

    pass
