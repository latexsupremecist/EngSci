# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.

Created by Haoyuan Shi @ 10:45, 1/26/2024
"""

import numpy as np
import matplotlib.pyplot as plt

#angles = np.arange(0,200,20)
angles_9090 = [0,20,25,30,32,33,34,35,40]
angles_00 = [0,20,25,30,32,33,34,40]


coinc_ave_lst_90=[]
coinc_ave_lst_00=[]

coinc_ave_uncer_lst_90=[]
coinc_ave_uncer_lst_00=[]

for angle in angles_9090:
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
    
    # rounding
    digits = -int(np.floor(np.log10(uncer)))
    uncer = round(uncer, digits)
    coinc_ave = round(coinc_ave, digits)
    
    if digits <= 0:
        uncer = int(uncer)
        coinc_ave = int(coinc_ave)
    
    coinc_ave_lst_90.append(coinc_ave)
    coinc_ave_uncer_lst_90.append(uncer)

    print("*"*20)
    print(f"Filename: {file_name}")
    print(f"Coincidences are {coinc_ave} +- {uncer}")
    
#angles = np.arange(0,200,20)

for angle in angles_00:
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
    
    # rounding
    digits = -int(np.floor(np.log10(uncer)))
    uncer = round(uncer, digits)
    coinc_ave = round(coinc_ave, digits)
    
    if digits <= 0:
        uncer = int(uncer)
        coince_ave = int(coinc_ave)
        
    coinc_ave_lst_00.append(coinc_ave)
    coinc_ave_uncer_lst_00.append(uncer)
    #print(len(coinc))
    print("*"*20)
    print(f"Filename: {file_name}")
    print(f"Coincidences are {coinc_ave} +- {uncer}")
    
plt.errorbar(angles_9090, coinc_ave_lst_90, \
        yerr=coinc_ave_uncer_lst_90,label='P9090')
plt.errorbar(angles_00, coinc_ave_lst_00, \
        yerr=coinc_ave_uncer_lst_00,label='P00')

plt.xlabel('HWP Angle')
plt.ylabel('Count')
plt.title('HWP Counting vs. Angle')
plt.legend()



