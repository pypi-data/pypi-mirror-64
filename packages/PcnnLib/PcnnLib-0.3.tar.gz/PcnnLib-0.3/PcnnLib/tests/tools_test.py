import unittest
import numpy as np

from PcnnLib.tools.spike_collector import collect_spikes


class TestTools(unittest.TestCase):

    def test_spike_collector_collect_correctly(self):
        spike_packages = [
            [
                [0, 1, 1],
                [1, 1, 1],
                [1, 1, 0]
            ],
            [
                [1, 1, 0],
                [1, 1, 1],
                [0, 1, 0]
            ],
            [
                [0, 1, 0],
                [1, 1, 1],
                [0, 1, 1]
            ]
        ]
        actual_collected_spikes = collect_spikes(spike_packages, 2)
        expected_collected_spikes = [
            [0, 1, 0],
            [1, 1, 1],
            [0, 1, 0]
        ]
        np.testing.assert_array_equal(actual_collected_spikes, expected_collected_spikes)