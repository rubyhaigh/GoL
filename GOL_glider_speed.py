# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 20:57:20 2023

@author: Ruby
"""

import numpy as np
import math
import random
import sys
import scipy
import scipy.optimize
import matplotlib.pyplot as plt

from GOL import *

#read data 
with open("com_list.txt") as f:
    com = f.readlines()

#isolate the values
com= [com[i].rstrip().lstrip() for i in range(len(com))]
com = [com[i].split() for i in range(len(com))]
positions = (np.array(com)).astype(float)

#times
with open("iter_list.txt") as f:
    iters = f.readlines()
    
time = [iters[i].rstrip().lstrip() for i in range(len(iters))]
time = (np.array(iters).astype(float))


speed_list = []
speed_list_swap = []
redundancy = 0


#find concurrent points, that don't cross a boundary, to average over
for i in range(len(positions)):
    if (i%5) == 0:
        print("Sweep {}/{}".format(i, len(positions)))
        
    if (i!= 0):
        #x and y values should both increase, check for boundary by comparig value with previous
        if ((positions[i][0] > positions[i-1][0]) and (positions[i][1] > positions[i-1][1])):
            speed_list_swap.append([positions[i][0], positions[i][1]])
            
        else: #at a boundary - check if current list is larger than original
            if (len(speed_list_swap) > len(speed_list)):
                speed_list = speed_list_swap
                speed_list_swap = []
                #reset redundancy
                redundancy = 0
                
            else:
                speed_list_swap = []
                redundancy += 1
     
       
    if redundancy == 1:
        
        print("Max list found")
        
        break;
        
#get a rough estimate for speed
deltaX = speed_list[0][0] - speed_list[-1:][0][0]
deltaY = speed_list[0][1] - speed_list[-1:][0][1]
mag_delta = np.sqrt(deltaX**2 + deltaY**2)

iter_no = len(speed_list)*10
speed = mag_delta/iter_no
print("Speed determined from 2 points: {}".format(speed))

#calculate speed by fitting
#def linear function
def lin_func(x, m, c):
    return m*x + c

time_list = time[:len(speed_list)]
x_list = np.array(speed_list)[:,0]
y_list = np.array(speed_list)[:,1]

#x fitting
popt_x, pcov_x = scipy.optimize.curve_fit(lin_func, time_list, x_list)
#y fitting
popt_y, pcov_y = scipy.optimize.curve_fit(lin_func, time_list, y_list)

av_speed = np.sqrt(popt_x[0]**2 + popt_y[0]**2)
print("Speed determined from fit: {}".format(av_speed))


#plot x fit
plt.plot(time_list, lin_func(time_list, *popt_x), 'g--', label='fit: m=%5.3f, c=%5.3f, ' % tuple(popt_x))
plt.scatter(time_list, x_list, label="Data")
plt.xlabel("Iteration number")
plt.ylabel("X position")
plt.title("Flight of glider across X coordinates with fitting")
plt.legend()
#plt.savefig("gliderwithfit.png")
plt.show()