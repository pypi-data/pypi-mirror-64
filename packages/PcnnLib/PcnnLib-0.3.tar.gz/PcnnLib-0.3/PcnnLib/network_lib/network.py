from PcnnLib.network_lib.connection import Connection
import math

from PcnnLib.network_lib.statistic_record import StatisticRecord


class Network:
    def __init__(self, fast_linking, metrics):
        self.FAST_LINKING = fast_linking
        self._metrics = metrics
        self._neurons = None

    def init_layer(self, layer_shape, neuron_factory):
        self._neurons = neuron_factory.create_neurons(layer_shape)
        frames = []
        for i in range(layer_shape[0]):
            for j in range(layer_shape[1]):
                if j - 1 >= 0:
                    neuron00 = self._neurons[i - 1][j - 1] if (i - 1 >= 0) else None
                    neuron10 = self._neurons[i][j - 1]
                    neuron20 = self._neurons[i + 1][j - 1] if (i + 1 < layer_shape[0]) else None
                else:
                    neuron00 = None
                    neuron10 = None
                    neuron20 = None

                neuron01 = self._neurons[i - 1][j] if (i - 1 >= 0) else None
                neuron11 = self._neurons[i][j]
                neuron21 = self._neurons[i + 1][j] if (i + 1 < layer_shape[0]) else None

                if j + 1 < layer_shape[1]:
                    neuron02 = self._neurons[i - 1][j + 1] if (i - 1 >= 0) else None
                    neuron12 = self._neurons[i][j + 1]
                    neuron22 = self._neurons[i + 1][j + 1] if (i + 1 < layer_shape[0]) else None
                else:
                    neuron02 = None
                    neuron12 = None
                    neuron22 = None

                frame = [
                    [neuron00, neuron01, neuron02],
                    [neuron10, neuron11, neuron12],
                    [neuron20, neuron21, neuron22]
                ]
                frames.append(frame)

        for frame in frames:
            weight = 1 / math.sqrt(2)
            self.__connect(frame[1][1], frame[0][1], 1)
            self.__connect(frame[1][1], frame[1][0], 1)
            self.__connect(frame[1][1], frame[1][2], 1)
            self.__connect(frame[1][1], frame[2][1], 1)

            self.__connect(frame[1][1], frame[0][0], weight)
            self.__connect(frame[1][1], frame[2][0], weight)
            self.__connect(frame[1][1], frame[0][2], weight)
            self.__connect(frame[1][1], frame[2][2], weight)

    def iterate(self, spikes, mask_spikes):
        result = []
        for i in range(len(spikes)):
            row = []
            for j in range(len(spikes[0])):
                spike = self._neurons[i][j].process_spike(spikes[i][j])
                row.append(spike)
            result.append(row)

        if self.FAST_LINKING:
            changes = True
            while changes:
                changes = False
                next_result = []
                for i in range(len(spikes)):
                    row = []
                    for j in range(len(spikes[0])):
                        curr_res = self._neurons[i][j].process_spike_fast_linking()
                        row.append(curr_res)
                        changes |= result[i][j] != curr_res
                    next_result.append(row)
                result = next_result

        total_threshold = 0
        for i in range(len(spikes)):
            for j in range(len(spikes[0])):
                total_threshold += self._neurons[i][j].recompute_threshold(result[i][j])

        for metric in self._metrics:
            metric.add_iteration(StatisticRecord(result, mask_spikes, total_threshold))

        return result

    def __connect(self, main_neuron, neuron, weight):
        if neuron is not None:
            conn = Connection(weight, 1, 0)
            main_neuron.connect_output(conn)
            neuron.connect_input(conn)
