from PcnnLib.helpers.file_helpers import get_filename, find_file
from PcnnLib.image_preprocessing.image_converters import read_img, resize_img, to_grayscale, to_normal_spikes


class DirectoryPipeline:
    def __init__(self, image_size, flow_images_dir_path, flow_masks_dir_path=None):
        self.IMAGE_SIZE = image_size
        import os
        self._dir_iterator = os.scandir(flow_images_dir_path)
        self._flow_masks_dir_path = flow_masks_dir_path

    def __iter__(self):
        return self

    def __next__(self):
        entry = next(self._dir_iterator)
        while entry.is_file() is False:
            entry = next(self._dir_iterator)

        img = read_img(entry.path).convert("RGB")
        img = resize_img(img, self.IMAGE_SIZE)
        img = to_grayscale(img)
        spikes = to_normal_spikes(img)

        if self._flow_masks_dir_path is None:
            mask_spikes = None
        else:
            mask_path = find_file(self._flow_masks_dir_path, get_filename(entry.path))
            if mask_path is None:
                return spikes, None
            img = read_img(mask_path).convert("RGB")
            img = resize_img(img, self.IMAGE_SIZE)
            mask_spikes = to_normal_spikes(img)

        return spikes, mask_spikes
