import os

from PcnnLib.helpers.file_helpers import find_file
from PcnnLib.image_preprocessing.image_converters import read_img, resize_img, to_grayscale, to_normal_spikes


class ImagesPipeline:
    def __init__(self, image_size, flow_images_dir_path, flow_image_names, flow_masks_dir_path=None):
        self.IMAGE_SIZE = image_size
        self._flow_image_names = flow_image_names
        self._image_index = 0
        self._flow_images_dir_path = flow_images_dir_path
        self._flow_masks_dir_path = flow_masks_dir_path

    def __iter__(self):
        return self

    def __next__(self):
        if self._image_index > len(self._flow_image_names) - 1:
            return None
        filename = self._flow_image_names[self._image_index]
        self._image_index += 1
        img_path = os.path.join(self._flow_images_dir_path, filename)
        img = read_img(img_path).convert("RGB")
        img = resize_img(img, self.IMAGE_SIZE)
        img = to_grayscale(img)
        spikes = to_normal_spikes(img)

        if self._flow_masks_dir_path is None:
            mask_spikes = None
        else:
            mask_path = find_file(self._flow_masks_dir_path, filename)
            if mask_path is None:
                return spikes, None
            img = read_img(mask_path).convert("RGB")
            img = resize_img(img, self.IMAGE_SIZE)
            mask_spikes = to_normal_spikes(img)

        return spikes, mask_spikes
