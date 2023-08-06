from PcnnLib.network_lib.connection import Connection


def decompose_connections(connections):
    return [(conn.spike, conn.weight_l, conn.weight_f) for conn in connections]


class SimpleNeuron:
    def __init__(self, linking_scale, linking_strength, threshold_scale, threshold_decay_step):
        self.internal_state = 0
        self.threshold = 0
        self._self_connection = Connection(1, 1, 0)
        self._input_connections = [self._self_connection]
        self._output_connections = [self._self_connection]
        self.feeding_result = 0
        self.linking_result = 0
        self.LINKING_SCALE = linking_scale
        self.THRESHOLD_SCALE = threshold_scale
        self.LINKING_STRENGTH = linking_strength
        self.threshold_decay_step = threshold_decay_step

    def connect_input(self, input_connection):
        self._input_connections.append(input_connection)

    def connect_output(self, output_connection):
        self._output_connections.append(output_connection)

    def process_spike(self, input_stimulus):
        self.feeding_result = input_stimulus
        self.linking_result = self.LINKING_SCALE * sum(connection.spike * connection.weight_l for connection in self._input_connections)
        self.internal_state = self.feeding_result * (1 + self.LINKING_STRENGTH * self.linking_result)
        spike = 1 if (self.internal_state > self.threshold) else 0
        for conn in self._output_connections:
            conn.spike = spike
        return spike

    def process_spike_fast_linking(self):
        self.linking_result = self.LINKING_SCALE * sum(connection.spike * connection.weight_l for connection in self._input_connections)
        self.internal_state = self.feeding_result * (1 + self.LINKING_STRENGTH * self.linking_result)
        spike = 1 if (self.internal_state > self.threshold) else 0
        for conn in self._output_connections:
            conn.spike = spike
        return spike

    def recompute_threshold(self, spike):
        self.threshold -= self.threshold_decay_step
        if self.threshold < 0:
            self.threshold = 0

        if spike > 0:
            if self.threshold < 1:
                self.threshold = 1
            self.threshold *= self.THRESHOLD_SCALE
        return self.threshold
