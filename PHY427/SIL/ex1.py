import numpy as np
import matplotlib.pyplot as plt

data1 = np.loadtxt('ex1.csv', delimiter=',', skiprows=1)

x1 = data1[:, 0]
y1 = data1[:, 1]

data2 = np.loadtxt('ex1_2.csv', delimiter=',', skiprows=1)

x2 = data2[:, 0]
y2 = data2[:, 1]

plt.plot(x1, y1, label="Measurement 1")
plt.plot(x2, y2, label="Measurement 2")
plt.xlabel("Voltage (V)")
plt.ylabel("Current (uA)")
plt.legend()
plt.show()
