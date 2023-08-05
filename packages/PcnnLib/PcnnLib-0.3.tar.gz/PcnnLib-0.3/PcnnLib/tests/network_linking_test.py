import unittest
from PcnnLib.network_lib.network import Network
from PcnnLib.network_lib.neuron_factories.full_neuron_factory import FullNeuronFactory


class TestNetworkLinking(unittest.TestCase):

    def assert_connections(self, target_neuron, neuron):
        target_input_connections = target_neuron.input_connections
        target_output_connections = target_neuron.output_connections
        input_connections = neuron.input_connections
        output_connections = neuron.output_connections
        common_connections = set(target_input_connections) & set(output_connections)
        self.assertEqual(len(common_connections), 1)
        common_connections = set(target_output_connections) & set(input_connections)
        self.assertEqual(len(common_connections), 1)

    def test_neurons_connected_correctly(self):
        nn = Network(True)
        neuron_factory = FullNeuronFactory(1, 1, 1, 1, 1, 1, 1)
        nn.init_layer((10, 10), neuron_factory)
        width = len(nn._neurons)
        height = len(nn._neurons)
        self.assert_connections(nn._neurons[0][0], nn._neurons[1][1])
        self.assert_connections(nn._neurons[0][height - 1], nn._neurons[1][height - 1])
        self.assert_connections(nn._neurons[width - 1][height - 1], nn._neurons[width - 2][height - 2])
