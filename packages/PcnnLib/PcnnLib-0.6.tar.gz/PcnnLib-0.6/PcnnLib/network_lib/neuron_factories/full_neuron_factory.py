from PcnnLib.network_lib.neurons.full_neuron import FullNeuron


class FullNeuronFactory:
    def __init__(self,
                 feeding_scale,
                 linking_scale,
                 threshold_scale,
                 linking_strength,
                 af,
                 al,
                 at):
        self.FEEDING_SCALE = feeding_scale
        self.LINKING_SCALE = linking_scale
        self.THRESHOLD_SCALE = threshold_scale
        self.LINKING_STRENGTH = linking_strength
        self.AF = af
        self.AL = al
        self.AT = at

    def create_neurons(self, shape):
        return [
            [
                FullNeuron(
                    self.FEEDING_SCALE,
                    self.LINKING_SCALE,
                    self.THRESHOLD_SCALE,
                    self.LINKING_STRENGTH,
                    self.AF,
                    self.AL,
                    self.AT)
                for j in range(shape[1])
            ] for i in range(shape[0])
        ]
