import math
import matplotlib.pyplot as plt
import numpy as np

data = [[1, 10, 4], [1, 12, 21], [2, 8, 38], [1, 26, 15], [1, 23, 32], [1, 24, 23], [2, 7, 29], [2, 9, 36], [2, 10, 29], [2, 11, 24], [1, 12, 39], [2, 9, 40]]
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


def parameters(data):

    stdev, stdeverr = 0, 0

    x, xerr, y, yerr = [datum[0] for datum in data], [datum[1] ** 2 for datum in data], [datum[2] for datum in data], [datum[3] ** 2 for datum in data]
    xMean, xMeanerr, yMean, yMeanerr = sum(x)/len(x), math.sqrt(sum(xerr))/len(xerr), sum(y)/len(y), math.sqrt(sum(yerr))/len(yerr)

    for i in range(len(x)):
        entry = data[i][0]
        err = data[i][1]
        stdev += (entry - xMean) ** 2
        stdeverr += 2 * (entry - xMean) * math.sqrt(err ** 2 + xMeanerr ** 2)
    stdev = math.sqrt(stdev/(len(x) - 1))
    stdeverr /= 2 * stdev * (len(x) - 1)
    
    return xMean, xMeanerr, yMean, yMeanerr, stdev, stdeverr

units = toUnits(data, calibration, uncertainty)
print(parameters(units))
