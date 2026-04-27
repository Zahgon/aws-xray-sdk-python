import threading

from .reservoir import Reservoir
from aws_xray_sdk.core.utils.search_pattern import wildcard_match


class SamplingRule:
    """
    Data model for a single centralized sampling rule definition.
    """
    def __init__(self, name, priority, rate, reservoir_size,
                 host=None, method=None, path=None, service=None,
                 service_type=None):
        self._name = name
        self._priority = priority
        self._rate = rate
        self._can_borrow = not not reservoir_size

        self._host = host
        self._method = method
        self._path = path
        self._service = service
        self._service_type = service_type

        self._reservoir = Reservoir()
        self._reset_statistics()

        self._lock = threading.Lock()

    def match(self, sampling_req):
        """
        Determines whether or not this sampling rule applies to the incoming
        request based on some of the request's parameters.
        Any ``None`` parameter provided will be considered an implicit match.
        """
        if sampling_req is None:
            return False

        host = sampling_req.get('host', None)
        method = sampling_req.get('method', None)
        path = sampling_req.get('path', None)
        service = sampling_req.get('service', None)
        service_type = sampling_req.get('service_type', None)

        return (not host or wildcard_match(self._host, host)) \
            and (not method or wildcard_match(self._method, method)) \
            and (not path or wildcard_match(self._path, path)) \
            and (not service or wildcard_match(self._service, service)) \
            and (not service_type or wildcard_match(self._service_type, service_type))

    def is_default(self):
        # ``Default`` is a reserved keyword on X-Ray back-end.
        return self.name == 'Default'

    def snapshot_statistics(self):
        """
        Take a snapshot of request/borrow/sampled count for reporting
        back to X-Ray back-end by ``TargetPoller`` and reset those counters.
        """
        pass

    def merge(self, rule):
        """
        Migrate all stateful attributes from the old rule
        """
        with self._lock:
            self._request_count = rule.request_count
            self._borrow_count = rule.borrow_count
            self._sampled_count = rule.sampled_count
            self._reservoir = rule.reservoir
            rule.reservoir = None

    def ever_matched(self):
        """
        Returns ``True`` if this sample rule has ever been matched
        with an incoming request within the reporting interval.
        """
        pass

    def time_to_report(self):
        """
        Returns ``True`` if it is time to report sampling statistics
        of this rule to refresh quota information for its reservoir.
        """
        pass

    def increment_request_count(self):
        with self._lock:
            self._request_count += 1

    def increment_borrow_count(self):
        with self._lock:
            self._borrow_count += 1

    def increment_sampled_count(self):
        with self._lock:
            self._sampled_count += 1

    def _reset_statistics(self):
        pass

    @property
    def rate(self):
        pass

    @rate.setter
    def rate(self, v):
        pass

    @property
    def name(self):
        pass

    @property
    def priority(self):
        pass

    @property
    def reservoir(self):
        pass

    @reservoir.setter
    def reservoir(self, v):
        pass

    @property
    def can_borrow(self):
        pass

    @property
    def request_count(self):
        pass

    @property
    def borrow_count(self):
        pass

    @property
    def sampled_count(self):
        pass
