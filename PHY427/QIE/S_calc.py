# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 11:32:29 2024

@author: student
"""

import numpy as np
import matplotlib.pyplot as plt

def get_E(L, U):
    numerator = L[0] + L[2] - L[1] - L[3]
    denom = L[0] + L[2] + L[1] + L[3] - 345.4
    uncer = np.sqrt(U[0]**2 + U[1]**2 + U[2]**2 + U[3]**2)
    return np.array([numerator / denom, uncer])

def get_S(L):
    s = L[0][0] + L[1][0] + L[2][0] + L[3][0]
    uncer = np.sqrt(L[0][1]**2 + L[1][1]**2 + L[2][1]**2 + L[3][1]**2)
    return s, uncer

#angles = np.arange(0,200,20)

file_names = ['ab','a+90b','a+90b+90','ab+90']
folder_names = ['-45-22.5', '-45+22.5', '0-22.5', '0+22.5']

E = []

for folder in folder_names:
    coinc_ave_lst_S=[]
    coinc_ave_uncer_lst_S=[]
    coinc = []
    for file_name in file_names:
        path = 'session7/'+ folder + '/' + file_name+ '.csv'
        with open(path, 'r') as data:
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
    
        # # rounding
        # digits = -int(np.floor(np.log10(uncer)))
        # uncer = round(uncer, digits)
        # coinc_ave = round(coinc_ave, digits)
    
        # if digits <= 0:
        #     uncer = int(uncer)
        #     coinc_ave = int(coinc_ave)
    
        coinc_ave_lst_S.append(coinc_ave)
        coinc_ave_uncer_lst_S.append(uncer)

        print("*"*20)
        print(f"Filename: {path}")
        print(f"Coincidences are {coinc_ave} +- {uncer}")
    E.append(get_E(coinc_ave_lst_S, coinc_ave_uncer_lst_S))

S = get_S(E)
print(S)
