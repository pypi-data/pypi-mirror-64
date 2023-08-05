import unittest

from PcnnLib.network_lib.connection import Connection
from PcnnLib.network_lib.neurons.full_neuron import FullNeuron


class TestNeuron(unittest.TestCase):

    def test_neuron_all_stimulus_spike(self):
        neuron = FullNeuron(0.125, 0.125, 12, 1, 0.1, 0.1, 0.1)
        for _ in range(8):
            connection = Connection(1, 1, 1)
            neuron.connect_input(connection)
        stimulus = 1
        result = neuron.process_spike(stimulus)
        self.assertEqual(result, 1)
        neuron.recompute_threshold(result)
        result = neuron.process_spike(stimulus)
        self.assertEqual(result, 0)

    def test_neuron_only_feeding_stimulus_spike(self):
        neuron = FullNeuron(1, 1, 1.9, 1, 0.1, 0.1, 0.1)
        for _ in range(8):
            connection = Connection(1, 1, 0)
            neuron.connect_input(connection)
        stimulus = 1
        result = neuron.process_spike(stimulus)
        self.assertEqual(result, 1)
        neuron.recompute_threshold(result)
        result = neuron.process_spike(stimulus)
        self.assertEqual(result, 1)
