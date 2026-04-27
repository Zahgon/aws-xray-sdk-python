import logging
from random import Random
import time
import threading

log = logging.getLogger(__name__)


class TargetPoller:
    """
    The poller to report the current statistics of all
    centralized sampling rules and retrieve the new allocated
    sampling quota and TTL from X-Ray service.
    """
    def __init__(self, cache, rule_poller, connector):
        self._cache = cache
        self._rule_poller = rule_poller
        self._connector = connector
        self._random = Random()
        self._interval = 10 # default 10 seconds interval on sampling targets fetch

    def start(self):
        poller_thread = threading.Thread(target=self._worker)
        poller_thread.daemon = True
        poller_thread.start()

    def _worker(self):
        pass

    def _do_work(self):
        pass

    def _get_candidates(self, all_rules):
        """
        Don't report a rule statistics if any of the conditions is met:
        1. The report time hasn't come(some rules might have larger report intervals).
        2. The rule is never matched.
        """
        pass

    def _get_jitter(self):
        """
        A random jitter of up to 0.1 seconds is injected after every run
        to ensure all poller calls eventually get evenly distributed
        over the polling interval window.
        """
        pass
