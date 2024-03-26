# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.

Created by Haoyuan Shi @ 10:45, 1/26/2024
"""

import numpy as np
import matplotlib.pyplot as plt

angles = np.arange(0,200,20)

for angle in angles:
    coinc = []
    file_name = 'P9090/HWP' + str(angle) + '.csv'
    with open(file_name, 'r') as data:
        data.readline() # Header
        line = data.readline().strip() #ist line
        while line != '':
            data_line = line.split(',')
            raw = float(data_line[0])
            correction = float(data_line[1])
            coinc.append(raw - correction)
            line = data.readline().strip()
    coinc_ave = np.average(coinc)
    uncer = np.sqrt(coinc_ave/len(coinc))
    #print(len(coinc))
    print("*"*20)
    print(file_name)
    print(coinc_ave, uncer)
    
    angles = np.arange(0,200,20)

for angle in angles:
    coinc = []
    file_name = 'P00/HWP' + str(angle) + '.csv'
    with open(file_name, 'r') as data:
        data.readline() # Header
        line = data.readline().strip() #ist line
        while line != '':
            data_line = line.split(',')
            raw = float(data_line[0])
            correction = float(data_line[1])
            coinc.append(raw - correction)
            line = data.readline().strip()
    coinc_ave = np.average(coinc)
    uncer = np.sqrt(coinc_ave/len(coinc))
    #print(len(coinc))
    print("*"*20)
    print(file_name)
    print(coinc_ave, uncer)