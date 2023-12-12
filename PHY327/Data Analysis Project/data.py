import math
import matplotlib.pyplot as plt
import numpy as np

data = [[1, 10, 4], [1, 12, 21], [2, 8, 38], [1, 26, 15], [1, 23, 32], [1, 24, 23], [2, 7, 29], [2, 9, 36], [2, 10, 29], [2, 11, 24], [1, 12, 39], [2, 9, 40]]

x = np.array([7.09, 10.75, 23.70, 21.67, 12.79, 20.45, 25.31, 18.96, 8.42, 7.82, 9.04, 7.17])
y = np.array([11.71, 25.71, 13.03, 20.10, 37.15, 25.53, 9.34, 36.00, 29.13, 35.51, 17.79, 27.33])
s = np.array([1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2])

# data = [[s[i],x[i],y[i]] for i in range(12)]

calibration = [26/19, 26/(19**2)]
uncertainty = 1


def toUnits(data, calibration, uncertainty):
    ret = []
    for entry in data:
        s, x, y = entry[0], entry[1], entry[2]

        hor = x * s * calibration[0]
        hor_err = s * math.sqrt((x * calibration[1]) ** 2 + (uncertainty * calibration[0]) ** 2)
        ver = y * s * calibration[0]
        ver_err = s * math.sqrt((y * calibration[1]) ** 2 + (uncertainty * calibration[0]) ** 2)
        ret.append([hor, hor_err, ver, ver_err])
    ret = sorted(ret, key=lambda x: x[0])
    return ret


def predNormal(x, xMean, yMean, stdev):

    y, yerr = [], []

    for entry in x:
        y.append(yMean * math.exp(-(entry - xMean) ** 2 / (2 * stdev ** 2)))
        yerr.append(0)
    return y, yerr


def predLog(x, xMean, yMean, stdev):

    y, yerr = [], []
    logMean = math.log(xMean)

    for entry in x:
        y.append(yMean * xMean * math.exp(-(math.log(entry) - logMean) ** 2 / (2 * stdev ** 2)) / entry)
        yerr.append(0)
    return y, yerr


def predLap(x, xMean, yMean, stdev):

    y, yerr = [], []

    for entry in x:
        y.append(yMean * math.exp(-abs(entry - xMean) / stdev))
        yerr.append(0)
    return y, yerr


def plotFit(data):

    stdev, stdeverr = 0, 0

    x, xerr, y, yerr = [datum[0] for datum in data], [datum[1] for datum in data], [datum[2] for datum in data], [datum[3] for datum in data]
    xMean, xMeanerr, yMean, yMeanerr = sum(x)/len(x), sum(xerr)/len(xerr), sum(y)/len(y), sum(yerr)/len(yerr)

    for i in range(len(x)):
        entry = data[i][0]
        err = data[i][1]
        stdev += (entry - xMean) ** 2
        stdeverr += 2 * (entry - xMean) * (err + xMeanerr)
    stdev = math.sqrt(stdev/(len(x) - 1))
    stdeverr /= 2 * stdev * (len(x) - 1)

    yNormal, yNormalErr = predNormal(x, xMean, yMean, stdev)
    yLog, yLogErr = predLog(x, xMean, yMean, stdev)
    yLap, yLapErr = predLap(x, xMean, yMean, stdev)

    # plot
    plt.plot(x, y, label='Data', color='blue')
    plt.plot(x, yNormal, label='Normal', color='red')
    plt.plot(x, yLog, label='Lognormal', color='green')
    plt.plot(x, yLap, label='Laplace', color='orange')

    # left = min(0, u_max)
    # right = max(0, u_max)

    # plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    plt.xlabel("x")
    plt.ylabel("y")
    # ax.set(xlim=(left, right), ylim=(-radius, radius))
    plt.suptitle("Plot of Actual Data and Expected y According to Fits")


    print(xMean, yMean, stdev)
    plt.legend()
    # plt.show()


units = toUnits(data, calibration, uncertainty)
plotFit(units)
