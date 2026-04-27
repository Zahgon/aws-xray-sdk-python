import binascii
import os
import time
from datetime import datetime

import botocore.session
from botocore import UNSIGNED
from botocore.client import Config

from .sampling_rule import SamplingRule
from aws_xray_sdk.core.models.dummy_entities import DummySegment
from aws_xray_sdk.core.context import Context


class ServiceConnector:
    """
    Connector class that translates Centralized Sampling poller functions to
    actual X-Ray back-end APIs and communicates with X-Ray daemon as the
    signing proxy.
    """
    def __init__(self):
        self._xray_client = self._create_xray_client()
        self._client_id = binascii.b2a_hex(os.urandom(12)).decode('utf-8')
        self._context = Context()

    def _context_wrapped(func):
        """
        Wrapping boto calls with dummy segment. This is because botocore
        has two dependencies (requests and httplib) that might be
        monkey-patched in user code to capture subsegments. The wrapper
        makes sure there is always a non-sampled segment present when
        the connector makes an  AWS API call using botocore.
        This context wrapper doesn't work with asyncio based context
        as event loop is not thread-safe.
        """
        pass

    @_context_wrapped
    def fetch_sampling_rules(self):
        """
        Use X-Ray botocore client to get the centralized sampling rules
        from X-Ray service. The call is proxied and signed by X-Ray Daemon.
        """
        pass

    @_context_wrapped
    def fetch_sampling_target(self, rules):
        """
        Report the current statistics of sampling rules and
        get back the new assgiend quota/TTL froom the X-Ray service.
        The call is proxied and signed via X-Ray Daemon.
        """
        pass

    def setup_xray_client(self, ip, port, client):
        """
        Setup the xray client based on ip and port.
        If a preset client is specified, ip and port
        will be ignored.
        """
        if not client:
            client = self._create_xray_client(ip, port)
        self._xray_client = client

    @property
    def context(self):
        pass

    @context.setter
    def context(self, v):
        pass

    def _generate_reporting_docs(self, rules, now):
        pass

    def _dt_to_epoch(self, dt):
        """
        Convert a offset-aware datetime to POSIX time.
        """
        pass

    def _is_rule_valid(self, record):
        # We currently only handle v1 sampling rules.
        pass

    def _create_xray_client(self, ip='127.0.0.1', port='2000'):
        session = botocore.session.get_session()
        url = 'http://%s:%s' % (ip, port)
        return session.create_client('xray', endpoint_url=url,
                                     region_name='us-west-2',
                                     config=Config(signature_version=UNSIGNED),
                                     aws_access_key_id='', aws_secret_access_key=''
                                     )
