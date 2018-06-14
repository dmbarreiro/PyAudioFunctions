import numpy as np


def energy(signal, axis=0):
    """Calculates the energy or input signal
    Parameters:
    signal (numpy array): Input signal/s
    axis (int): Indicates direction of the summation
    """
    result = np.sum(np.square(abs(signal)), axis=axis)
    return result


def slice_spectrum(spectrum, freq_thresholds, fs, N, dft_size):
    """Splits input digital spectrum in frequency bands
    Parameters:
    spectrum (numpy array): Spectrum to be sliced
    freq_thresholds (list): Contains frequency tuples (initial, end) of the
    different chunks, these frequencies are excluded from the chunk.
    Example:
    [(0, 40)] will return frequency samples for frequencies > 0 and < 40
    fs (float): Sampling frequency
    N (int): Number of samples of the FFT
    """
    result_bands = list()
    hz_per_bin = fs/N
    frequency_bin = np.arange(dft_size) * hz_per_bin
    for band_init, band_end in freq_thresholds:
        band = np.where((frequency_bin > band_init) &
                        (frequency_bin < band_end))
        result_bands.append(band)
    return result_bands
