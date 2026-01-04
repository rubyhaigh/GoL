# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 13:35:24 2023

@author: Ruby
"""

import matplotlib.pyplot as plt
import numpy as np
import random
import sys

from GOL import *


equilibrium_list = []

for i in range(150):
    print("Processing Simulation {}...".format(i))
    equilibrium_list.append(gol_sim_run(50, 1000, 0, 1))
    print("Equilibrium found at {}".format(equilibrium_list[i]))
    
hist = plt.hist(equilibrium_list, bins=70)
plt.xlabel("Number of iterations")
plt.ylabel("Counts")
plt.title("Time for equilibrium for 150 Game of Life Simulations")
plt.savefig("equib_hist3.png")
plt.show()


pos_write(equilibrium_list, "equilibrium_list3.txt")