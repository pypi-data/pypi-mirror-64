from PcnnLib.network_lib.neurons.simple_neuron import SimpleNeuron


class SimpleNeuronFactory:
    def __init__(self,
                 linking_scale,
                 linking_strength,
                 threshold_scale,
                 threshold_decay_step):
        self.LINKING_SCALE = linking_scale
        self.LINKING_STRENGTH = linking_strength
        self.THRESHOLD_SCALE = threshold_scale
        self.THRESHOLD_DECAY_STEP = threshold_decay_step

    def create_neurons(self, shape):
        return [
            [
                SimpleNeuron(
                    self.LINKING_SCALE,
                    self.LINKING_STRENGTH,
                    self.THRESHOLD_SCALE,
                    self.THRESHOLD_DECAY_STEP)
                for j in range(shape[1])
            ] for i in range(shape[0])
        ]
