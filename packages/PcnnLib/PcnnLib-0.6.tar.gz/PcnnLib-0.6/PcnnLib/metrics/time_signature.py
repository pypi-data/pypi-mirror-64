from itertools import chain


class TimeSignature:
    def __init__(self):
        self._signature = []
        self._thresholds = []

    def add_iteration(self, stat_record):
        sgn_value = sum(chain.from_iterable(stat_record.spikes))
        self._signature.append(sgn_value)
        self._thresholds.append(stat_record.total_threshold)

    def get_signature(self):
        return self._signature

    def get_thresholds(self):
        return self._thresholds
