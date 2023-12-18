import numpy as np
import matplotlib.pyplot as plt


def DHe(temp, sv):
    return sv - 3.2106e-24 * np.sqrt(temp)


def pB(temp, sv):
    return 8.3328 * sv - 5.6e-22 * np.sqrt(temp)


def DT(temp, sv):
    return sv - 2.43e-23 * np.sqrt(temp)


def Lawsona(T, ratio):
    num = 1.34e18 * (1 + 1 / ratio)
    denom = np.log(T) - 2.1
    return num / denom


def Lawsond(T, k=1):
    num = 4.807 * T
    denom = 4.674e-34 * (np.log(T) - 2.1) - 5e-37 * np.sqrt(T) - 1e-36 * k * T ** 2
    return num/denom


temp = np.array([1, 10, 20, 40, 80, 200, 300])
DHesv = np.array([.692e-28, .626e-24, .273e-23, .826e-23, .193e-22, .462e-22, .650e-22])
DTsv = np.array([.830e-28, .582e-24, .243e-23, .721e-23, .167e-22, .414e-22, .585e-22])

first = DHe(temp, DHesv)
second = pB(temp, DHesv)
third = DT(temp, DTsv)


def q1():
    while (True):
        print("What is T?   ")
        T = float(input())
        print("What is sv?  ")
        sv = float(input())
        print(pB(T, sv))


def q2():
    for i in range(len(temp)):
        print(f"Temp is {temp[i]}, difference is {third[i]}")


def q3a():
    T = np.linspace(10, 100)
    y1 = Lawsona(T, 0.5)
    y2 = Lawsona(T, 1)
    y3 = Lawsona(T, 1.5)
    y4 = Lawsona(T, 2)
    plt.plot(T, y1, linestyle="solid", label="Ti/Te = 0.5")
    plt.plot(T, y2, linestyle="dotted", label="Ti/Te = 1")
    plt.plot(T, y3, linestyle="dashed", label="Ti/Te = 1.5")
    plt.plot(T, y4, linestyle="dashdot", label="Ti/Te = 2")
    plt.xlabel("Ti (keV)")
    plt.ylabel("n tau (m^-3s)")
    plt.title("n tau verses Ti")
    plt.legend()
    plt.show()


def q3d():
    T = np.linspace(10, 100)
    y1 = Lawsond(T, 1)
    y2 = Lawsond(T, 0.01)
    plt.plot(T, y1, linestyle="dotted", label="K_cy = 1")
    plt.plot(T, y2, linestyle="solid", label="K_cy = 0.01")
    plt.xlabel("T (keV)")
    plt.ylabel("n tau (m^-3s)")
    plt.title("n tau verses T")
    plt.legend()
    plt.show()


q3d()
