import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal


def get_spectrum():
    current_directory = os.getcwd()
    file_list = os.listdir(current_directory)
    return [file for file in file_list if file.endswith(".csv")]


def plot_spectrum(fname_arr):
    for FNAME in fname_arr:
        plt.figure()
        spectrum = np.loadtxt(FNAME, delimiter=',', ndmin=2)
        x = np.array([item[0] for item in spectrum])
        y = np.array([item[1] for item in spectrum])
        peaks = signal.find_peaks(y, height=max(y)/20, distance=20, prominence=max(y)/20)

        plt.plot(x, y, color='b')
        peak_x = [x[i] for i in peaks[0]]
        peak_y = [y[i] for i in peaks[0]]
        plt.scatter(peak_x, peak_y, marker='x', color='r')
        plt.gca().invert_xaxis()
        plt.xlabel("Wavenumber (cm^-1)")
        plt.ylabel("Absorbance")
        plt.title(FNAME[:-4])
    plt.show()
    return


spectrum_arr = get_spectrum()
plot_spectrum(spectrum_arr)
