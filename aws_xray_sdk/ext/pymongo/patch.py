# Copyright © 2018 Clarity Movement Co. All rights reserved.
from pymongo import monitoring
from aws_xray_sdk.core import xray_recorder


class XrayCommandListener(monitoring.CommandListener):
    """
    A listener that traces all pymongo db commands to AWS Xray.
    Creates a subsegment for each mongo db conmmand.

    name: 'mydb@127.0.0.1:27017'
    records all available information provided by pymongo,
    except for `command` and `reply`. They may contain business secrets.
    If you insist to record them, specify `record_full_documents=True`.
    """

    def __init__(self, record_full_documents):
        super().__init__()
        self.record_full_documents = record_full_documents

    def started(self, event):
        pass

    def succeeded(self, event):
        pass

    def failed(self, event):
        pass


def patch(record_full_documents=False):
    # ensure `patch()` is idempotent
    if hasattr(monitoring, '_xray_enabled'):
        return
    setattr(monitoring, '_xray_enabled', True)
    monitoring.register(XrayCommandListener(record_full_documents))
