import numpy as np


class Mse:
    def __init__(self):
        self._results = []

    def add_iteration(self, stat_record):
        if stat_record.mask_spikes is None:
            return
        mse_sum = 0
        total_number = 0
        for i in range(len(stat_record.spikes)):
            for j in range(len(stat_record.spikes[0])):
                mse_sum += (stat_record.spikes[i][j] - stat_record.mask_spikes[i][j])**2
                total_number += 1

        self._results.append(1 / total_number * mse_sum)

    def get_metrics(self):
        return self._results

    def get_mean_metric(self):
        return np.mean(self._results)
