import numpy as np
from scipy.signal import get_window
import matplotlib.pyplot as plt
import pathmagic  # noqa
import stft
import utilFunctions as UF
import dsp_toolbox

eps = np.finfo(float).eps


def stft_onset(inputFile, window, M, N, H, freq_thresholds, show_plot=False, debug=False):
    """
    Inputs:
            inputFile (string): input sound file (monophonic with sampling rate of 44100)
            window (string): analysis window type (choice of rectangular, triangular, hanning, hamming,
                blackman, blackmanharris)
            M (integer): analysis window size (odd integer value)
            N (integer): fft size (power of two, bigger or equal than than M)
            H (integer): hop size for the STFT computation
            freq_thresholds (list): Contains frequency tuples (initial, end) of the
            different chunks, these frequencies are excluded from the chunk.
            show_plot (boolean): enable/disable spectrogram, energy envelope and onset function visualization
            debug (boolean): enable/disable debug messages during execution

    Output:
            The function should return a numpy array with two columns, where the first column is the ODF
            computed on the low frequency band and the second column is the ODF computed on the high
            frequency band.
            ODF[:,0]: ODF computed in band 0 < f < 3000 Hz
            ODF[:,1]: ODF computed in band 3000 < f < 10000 Hz
    """

    # your code here

    fs, x = UF.wavread(inputFile)
    w = get_window(window, M)
    dBX, pX = stft.stftAnal(x, w, N, H)

    X = 10**(dBX/20.0)
    dft_size = X[0, :].size
    if debug:
        print("Spectrogram shape = {}".format(X.shape))

    band_index = dsp_toolbox.slice_spectrum(X, freq_thresholds, fs, N, dft_size)
    if debug:
        print("band_index elements = {}".format(len(band_index)))

    onset_result = np.array([])
    energy_result = np.array([])
    for band in band_index:
        energy = dsp_toolbox.energy(X[:, band], axis=-1)
        energy[energy < eps] = eps
        db_energy = 10*np.log10(energy)
        odf_band = db_energy[1:] - db_energy[:-1]
        odf_band[odf_band < 0] = 0  # Half wave rectification
        odf_band = np.insert(odf_band, 0, 0)
        # add extra sample in the beginning to match with energy envelope size
        db_energy = np.reshape(db_energy, (db_energy.size, 1))
        odf_band = np.reshape(odf_band, (odf_band.size, 1))
        # print("db_energy shape = {}".format(db_energy.shape))
        # print("odf_band shape = {}".format(odf_band.shape))
        energy_result = db_energy if energy_result.size == 0 else np.concatenate((energy_result, db_energy), axis=0)
        onset_result = odf_band if onset_result.size == 0 else np.concatenate((onset_result, odf_band), axis=0)

    if debug:
        print("energy_result shape = {}".format(energy_result.shape))
        print("onset_result shape = {}".format(onset_result.shape))

    if show_plot:
        plt.figure(1, figsize=(9.5, 6))

        plt.subplot(311)
        numFrames = int(dBX[:, 0].size)
        frmTime = H*np.arange(numFrames)/float(fs)
        binFreq = np.arange(N/2+1)*float(fs)/N
        plt.pcolormesh(frmTime, binFreq, np.transpose(dBX))
        plt.title('Spectrogram')
        plt.autoscale(tight=True)

        plt.subplot(312)
        for i in range(np.size(energy_result, 1)):
            plt.plot(energy_result[:, i], label='band {}'.format(i))
        # plt.plot(frmTime, db_high_mx, label='high band')
        plt.title('Energy envelopes')
        plt.legend()
        plt.autoscale(tight=True)
        plt.show(block=False)

        plt.subplot(313)
        for i in range(np.size(onset_result, 1)):
            plt.plot(onset_result[:, i], label='band {}'.format(i))
        # plt.plot(frmTime, odf_high, label='high band')
        plt.title('Onset detection function')
        plt.legend()
        plt.autoscale(tight=True)
        plt.show(block=False)

    return onset_result
