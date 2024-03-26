import numpy as np


data = np.loadtxt("Pedestals\pedestal_1v2", max_rows=128)
noise = [pair[1] for pair in data]
mean = np.mean(noise)
stdev = np.std(noise, ddof=1)
print(f"Mean is {mean}, stdev is {stdev}")