import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal


def get_spectrum():
    current_directory = os.getcwd()
    elements = os.listdir(current_directory)
    ret = []
    for element in elements:
        if os.path.isdir(element):
            sub = os.listdir(element)
            temp = [file for file in sub if file.endswith(".csv")]
            temp = [element] + temp
            ret.append(temp)
        elif element.endswith(".csv"):
            ret.append(element)
    return ret


def avg(x):
    ret = []
    for i in range(len(x[0])):
        temp = 0
        for j in range(len(x)):
            temp += x[j][i]
        ret.append(temp / len(x))
    return np.array(ret)


def plot_spectrum(fname_arr):
    for item in fname_arr:
        plt.figure()
        if not isinstance(item, str):
            directory = item[0]
            spectrum = [np.loadtxt(directory + "/" + item[i], delimiter=',', ndmin=2) for i in range(1, len(item))]
            x, y = [], []
            for file in spectrum:
                x.append(np.array([term[0] for term in file]))
                y.append(np.array([term[1] for term in file]))
            x = avg(x)
            y = avg(y)
            title = item[0]
        else:
            spectrum = np.loadtxt(item, delimiter=',', ndmin=2)
            x = np.array([item[0] for item in spectrum])
            y = np.array([item[1] for item in spectrum])
            title = item[:-4]
        peaks = signal.find_peaks(y, distance=20, prominence=max(y)/20)
        if title.lower() == "air":
            peaks = signal.find_peaks(y, height=0.5)
        plt.title(title)
        print(f"{title} has peaks")
        wavenumber = [x[peak] for peak in peaks[0]]
        print(wavenumber)

        plt.plot(x, y, color='b')
        peak_x = [x[i] for i in peaks[0]]
        peak_y = [y[i] for i in peaks[0]]
        plt.scatter(peak_x, peak_y, marker='x', color='r')
        plt.gca().invert_xaxis()
        plt.xlabel("Wavenumber (cm^-1)")
        plt.ylabel("Absorbance")
    plt.show()
    return


spectrum_arr = get_spectrum()
plot_spectrum(spectrum_arr)
