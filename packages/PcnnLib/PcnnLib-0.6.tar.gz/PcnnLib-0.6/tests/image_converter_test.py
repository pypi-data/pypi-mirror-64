import os
import unittest

from PcnnLib.image_preprocessing.image_converters import read_img, to_binary_spikes, apply_mask, to_grayscale, to_spikes


class TestImageConverters(unittest.TestCase):
    def test_neurons_connected_correctly(self):
        img = read_img("./data/image.jpg")
        mask = to_grayscale(read_img("./data/mask.jpg"))
        expected_masked_img = read_img("./data/masked_img.jpg")
        mask_spikes = to_binary_spikes(mask)

        apply_mask(img, mask_spikes).save("./data/temp.jpg")
        actual_masked_img = read_img("./data/temp.jpg")

        self.assertEqual(actual_masked_img.tobytes(), expected_masked_img.tobytes())

    def tearDown(self):
        os.remove("./data/temp.jpg")
