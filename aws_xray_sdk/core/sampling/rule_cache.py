import threading
from operator import attrgetter

TTL = 60 * 60  # The cache expires 1 hour after the last refresh time.


class RuleCache:
    """
    Cache sampling rules and quota retrieved by ``TargetPoller``
    and ``RulePoller``. It will not return anything if it expires.
    """
    def __init__(self):

        self._last_updated = None
        self._rules = []
        self._lock = threading.Lock()

    def get_matched_rule(self, sampling_req, now):
        if self._is_expired(now):
            return None
        matched_rule = None
        for rule in self.rules:
            if(not matched_rule and rule.match(sampling_req)):
                matched_rule = rule
            if(not matched_rule and rule.is_default()):
                matched_rule = rule
        return matched_rule

    def load_rules(self, rules):
        # Record the old rules for later merging.
        with self._lock:
            self._load_rules(rules)

    def load_targets(self, targets_dict):
        pass

    def _load_rules(self, rules):
        oldRules = {}
        for rule in self.rules:
            oldRules[rule.name] = rule

        # Update the rules in the cache.
        self.rules = rules

        # Transfer state information to refreshed rules.
        for rule in self.rules:
            old = oldRules.get(rule.name, None)
            if old:
                rule.merge(old)

        # The cache should maintain the order of the rules based on
        # priority. If priority is the same we sort name by alphabet
        # as rule name is unique.
        self.rules.sort(key=attrgetter('priority', 'name'))

    def _load_targets(self, targets_dict):
        pass

    def _is_expired(self, now):
        # The cache is treated as expired if it is never loaded.
        if not self._last_updated:
            return True
        return now > self.last_updated + TTL

    @property
    def rules(self):
        pass

    @rules.setter
    def rules(self, v):
        pass

    @property
    def last_updated(self):
        pass

    @last_updated.setter
    def last_updated(self, v):
        pass
