from PcnnLib.image_preprocessing.directory_pipeline import DirectoryPipeline
from PcnnLib.image_preprocessing.images_pipeline import ImagesPipeline
from PcnnLib.metrics.mse import Mse
from PcnnLib.network_lib.network import Network
from PcnnLib.network_lib.neuron_factories.full_neuron_factory import FullNeuronFactory
import numpy as np


class GridSearch:
    def __init__(self):
        self._values = []

    def find_best_value(self, img_size, img_dir, mask_dir, neuron_params, target_param_name, min_value, max_value, step,
                        image_names=None):
        best_mse = None
        best_i = 0
        for i in np.arange(min_value, max_value, step):
            neuron_params[target_param_name] = i
            neuron_factory = FullNeuronFactory(**neuron_params)
            mse_metric = Mse()
            network = Network(fast_linking=True, metrics=[mse_metric])
            network.init_layer(img_size, neuron_factory)
            img_pipeline = DirectoryPipeline(img_size, img_dir, mask_dir) if image_names is None else ImagesPipeline(
                img_size, img_dir, image_names, mask_dir)

            for spikes, mask_spikes in img_pipeline:
                network.iterate(spikes, mask_spikes)

            current_mse = mse_metric.get_mean_metric()
            self._values.append(current_mse)
            if best_mse is None or current_mse > best_mse:
                best_mse = current_mse
                best_i = i
        return best_i, best_mse

    def get_values(self):
        return self._values
