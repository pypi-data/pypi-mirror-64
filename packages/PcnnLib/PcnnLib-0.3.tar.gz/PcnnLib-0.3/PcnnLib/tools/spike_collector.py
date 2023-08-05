import numpy as np


def collect_spikes(spikes_packages, threshold):
    i_n = len(spikes_packages[0])
    j_n = len(spikes_packages[0][0])
    frequences = np.zeros((i_n, j_n))

    for spikes in spikes_packages:
        for i in range(i_n):
            for j in range(j_n):
                frequences[i][j] += spikes[i][j]

    result = np.zeros((i_n, j_n))
    for i in range(i_n):
        for j in range(j_n):
            if frequences[i][j] > threshold:
                result[i][j] = 1

    return result
