import httpx

from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core.models import http
from aws_xray_sdk.ext.util import inject_trace_header, get_hostname


def patch():
    httpx.Client = _InstrumentedClient
    httpx.AsyncClient = _InstrumentedAsyncClient
    httpx._api.Client = _InstrumentedClient


class _InstrumentedClient(httpx.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._original_transport = self._transport
        self._transport = SyncInstrumentedTransport(self._transport)


class _InstrumentedAsyncClient(httpx.AsyncClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._original_transport = self._transport
        self._transport = AsyncInstrumentedTransport(self._transport)


class SyncInstrumentedTransport(httpx.BaseTransport):
    def __init__(self, transport: httpx.BaseTransport):
        self._wrapped_transport = transport

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        pass


class AsyncInstrumentedTransport(httpx.AsyncBaseTransport):
    def __init__(self, transport: httpx.AsyncBaseTransport):
        self._wrapped_transport = transport

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        pass
