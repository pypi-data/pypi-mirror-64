import math

from PcnnLib.network_lib.connection import Connection


def decompose_connections(connections):
    return [(conn.spike, conn.weight_l, conn.weight_f) for conn in connections]


class FullNeuron:
    def __init__(self, feeding_scale, linking_scale, threshold_scale, linking_strength, af, al, at):
        self.internal_state = 0
        self.threshold = 0
        self._self_connection = Connection(1, 1, 0)
        self._input_connections = [self._self_connection]
        self._output_connections = [self._self_connection]
        self.feeding_result = 0
        self.linking_result = 0
        self.LINKING_SCALE = linking_scale
        self.FEEDING_SCALE = feeding_scale
        self.THRESHOLD_SCALE = threshold_scale
        self.LINKING_STRENGTH = linking_strength
        self.AF = af
        self.AL = al
        self.AT = at

    def connect_input(self, input_connection):
        self._input_connections.append(input_connection)

    def connect_output(self, output_connection):
        self._output_connections.append(output_connection)

    def process_spike(self, input_stimulus):
        dec_connections = decompose_connections(self._input_connections)
        self.feeding_result = math.exp(-self.AF) * self.feeding_result + input_stimulus + self.FEEDING_SCALE * sum(
            r * wf for r, wl, wf in dec_connections)
        self.linking_result = math.exp(-self.AL) * self.linking_result + self.LINKING_SCALE * sum(
            r * wl for r, wl, wf in dec_connections)
        self.internal_state = self.feeding_result * (1 + self.LINKING_STRENGTH * self.linking_result)
        spike = 1 if (self.internal_state > self.threshold) else 0
        for conn in self._output_connections:
            conn.spike = spike
        return spike

    def process_spike_fast_linking(self):
        dec_connections = decompose_connections(self._input_connections)
        self.linking_result = self.LINKING_SCALE * sum(r * wl for r, wl, wf in dec_connections)
        self.internal_state = self.feeding_result * (1 + self.LINKING_STRENGTH * self.linking_result)
        spike = 1 if (self.internal_state > self.threshold) else 0
        for conn in self._output_connections:
            conn.spike = spike
        return spike

    def recompute_threshold(self, spike):
        self.threshold = math.exp(-self.AT) * self.threshold + self.THRESHOLD_SCALE * spike
        return self.threshold
