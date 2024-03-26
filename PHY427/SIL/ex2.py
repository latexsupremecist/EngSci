import numpy as np
import matplotlib.pyplot as plt


f_arr = [[0, "pedestal_0v"], [50, "pedestal_50v"], [100, "pedestal_100v"]]
x = [f[0] for f in f_arr]
mean = []
stdev = []

for [bias_voltage, fname] in f_arr:
    data = np.loadtxt(fname, delimiter='\t', max_rows=128)
    pedestal = [pair[0] for pair in data]
    noise = [pair[1] for pair in data]
    mean.append(np.mean(noise))
    stdev.append(np.std(noise, ddof=1))

print(f"Means are {mean}\nStdevs are {stdev}")
