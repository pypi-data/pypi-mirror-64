import numpy
from PIL import Image


def read_img(path):
    return Image.open(path)


def save_img(img, path):
    return img.save(path)


def resize_img(img, size):
    return img.resize((size[1], size[0]), Image.ANTIALIAS)


def spikes_to_img(spikes):
    """Convert 2d matrix of spikes to image.
    # Arguments
        spikes: 2d list with values between 0 and 255
    # Returns
        PIL image
    """
    arr = numpy.asarray([numpy.array(r, dtype=numpy.uint8) for r in spikes])
    img = Image.fromarray(arr)
    return img


def denormalize_spikes_scaled(spikes):
    arr = numpy.asarray([numpy.array(r) for r in spikes])
    normalize_item_vec = numpy.vectorize(lambda i: i * 255)
    return normalize_item_vec(arr)


def to_grayscale(img):
    return img.convert('L')


def to_spikes(img):
    return numpy.asarray(img)


def to_normal_spikes(img):
    spikes = to_spikes(img)
    maximum_stimulus = spikes.max()
    minimum_stimulus = spikes.min()
    delta = maximum_stimulus - minimum_stimulus
    normalize_item_vec = numpy.vectorize(lambda i: (float(i) - minimum_stimulus) / delta)
    spikes = normalize_item_vec(spikes)
    return spikes


def to_binary_spikes(img, fixed_threshold=None):
    spikes = to_spikes(img)
    if fixed_threshold is not None:
        normalize_item_vec = numpy.vectorize(lambda i: 1 if i > fixed_threshold else 0)
        spikes = normalize_item_vec(spikes)
        return spikes
    maximum_stimulus = spikes.max()
    minimum_stimulus = spikes.min()
    delta = maximum_stimulus - minimum_stimulus
    average = delta / 2 + minimum_stimulus
    normalize_item_vec = numpy.vectorize(lambda i: 1 if i > average else 0)
    spikes = normalize_item_vec(spikes)
    return spikes


def apply_mask(img, mask):
    """Apply a mask on an image. The area outside the mask turns black.
    # Arguments
        image: PIL image
        mask: PIL mask
    # Returns
        PIL masked image
    """
    img_arr = numpy.asarray(img)
    result = []
    for i in range(len(mask) - 1):
        row = []
        for j in range(len(mask[0]) - 1):
            row.append(numpy.array([0, 0, 0], dtype=numpy.uint8) if mask[i][j] == 0 else img_arr[i][j])
        result.append(row)
    return spikes_to_img(result)
