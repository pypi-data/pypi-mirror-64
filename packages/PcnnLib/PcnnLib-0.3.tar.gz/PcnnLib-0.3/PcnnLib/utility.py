from PcnnLib.image_preprocessing.image_converters import to_binary_spikes, to_grayscale, read_img, spikes_to_img, save_img, to_spikes, \
    to_normal_spikes
from PcnnLib.network_lib.network import Network
import argparse
import pyclustering


def main():
    parser = argparse.ArgumentParser(description='Filter image background.')
    parser.add_argument('--input', dest='input_path', help='input file path')
    parser.add_argument('--output', dest='output_path', help='output file path')

    args = parser.parse_args()
    img = read_img(args.input_path)
    img = to_grayscale(img)
    img_list = to_binary_spikes(img)
    nn = Network(1, 1, 30, 1, 0.1, 0.1, 0.8, True)
    nn.init_layer([len(img_list), len(img_list[0])])
    for i in range(4):
        print(f'iteration: {i}')
        output_img_list = nn.iterate(img_list)
        #output_img_list = denormalize_spikes(output_img_list)
        output_img = spikes_to_img(output_img_list)
        save_img(output_img, args.output_path + "_iter_" + str(i) + ".jpg")


if __name__ == "__main__":
    main()

