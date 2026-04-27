import logging
from random import Random
import time
import threading

log = logging.getLogger(__name__)

DEFAULT_INTERVAL = 5 * 60  # 5 minutes on sampling rules fetch


class RulePoller:

    def __init__(self, cache, connector):

        self._cache = cache
        self._random = Random()
        self._time_to_wait = 0
        self._time_elapsed = 0
        self._connector = connector

    def start(self):
        poller_thread = threading.Thread(target=self._worker)
        poller_thread.daemon = True
        poller_thread.start()

    def _worker(self):
        pass

    def wake_up(self):
        """
        Force the rule poller to pull the sampling rules from the service
        regardless of the polling interval.
        This method is intended to be used by ``TargetPoller`` only.
        """
        pass

    def _refresh_cache(self):
        pass

    def _reset_time_to_wait(self):
        """
        A random jitter of up to 5 seconds is injected after each run
        to ensure the calls eventually get evenly distributed over
        the 5 minute window.
        """
        pass
