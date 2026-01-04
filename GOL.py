# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 18:21:47 2023

@author: Ruby
"""

import matplotlib.pyplot as plt
import numpy as np
import random
import sys

def gol_array_rand(lattice_size):
    #create random Boolean 2d array
    array = np.zeros((lattice_size, lattice_size), dtype=bool)
    
    for i in range(lattice_size):
        for j in range(lattice_size):
            coinflip = round(random.uniform(0, 1))
            if (coinflip ==1):
                array[i, j] = True
    return array

def gol_array_osc(lattice_size):
    #define blinker
    if (lattice_size >= 5): #check lattixc is big enough to define oscillator
        array = np.zeros((lattice_size, lattice_size), dtype=bool)
        for i in range(lattice_size):
            for j in range(lattice_size):
                if (i%5 == 0) and (j%5 == 0 or j%5 == 1 or j%5 == 2):
                    array[i, j] = True
                else:
                    array[i, j] = False
        return array
    else:
        print("WARNING: not enough space to make oscillator, returning empty array...")
        array = np.zeros((lattice_size, lattice_size), dtype=bool)

def gol_array_osc2(lattice_size):
    #define initial conditions to reduce into a blinker
    if (lattice_size >= 15):
        array = np.zeros((lattice_size, lattice_size), dtype=bool)
        for i in range(lattice_size):
            for j in range(lattice_size):
                if (j==10) and (i==10 or i ==11 or i==12 or i ==13 or i ==14):
                    array[i, j] = True
                if (j==11) and (i==10 or i==14):
                    array[i, j] = True
                if (j==12) and (i==11 or i==12 or i==13):
                    array[i, j] = True
        return array
    else:
        print("WARNING: not enough space to make oscillator, returning empty array...")
        array = np.zeros((lattice_size, lattice_size), dtype=bool)
        
        
def gol_array_beehive(lattice_size):
    #define initial conditons to reduce into beehive 
    if (lattice_size >= 15):
        array = np.zeros((lattice_size, lattice_size), dtype=bool)
        for i in range(lattice_size):
            for j in range(lattice_size):
                if (i==9) and (j==13):
                    array[i, j] = True
                if (i==10) and (j==11 or j==12 or j==13 or j==14):
                    array[i, j] = True
                if (i==11) and (j==10 or j==11):
                    array[i, j] = True
        return array
    else:
        print("WARNING: not enough space to make beehive, returning empty array...")
        array = np.zeros((lattice_size, lattice_size), dtype=bool)

def gol_array_glider(lattice_size):
    #define glider
    array = np.zeros((lattice_size, lattice_size), dtype=bool)
    if (lattice_size >=3):
        for i in range(lattice_size):
            for j in range(lattice_size):
                if (i, j) == (0, 1):
                    array[i, j] = True
                if (i, j) == (1, 2):
                    array[i, j] = True
                if (i, j) == (2, 0):
                    array[i, j] = True
                if (i, j) == (2, 1):
                    array[i, j] = True
                if (i, j) == (2, 2):
                    array[i, j] = True
        return array
    else:
        print("WARNING: not enough space to make glider, returning empty array...")
        array = np.zeros((lattice_size, lattice_size), dtype=bool)
        
def nn_check(array, lattice_size, i, j):
    #only condider boundaries when adding as if goes to -1 will loop back round
    left = (i, j-1)
    right = (i, (j+1)%lattice_size)
    top = (i-1, j)
    bottom = ((i+1)%lattice_size, j)
    
    #DIAGONAL
    top_left = (i-1, j-1)
    top_right = (i-1, (j+1)%lattice_size)
    bottom_left = ((i+1)%lattice_size, j-1)
    bottom_right = ((i+1)%lattice_size, (j+1)%lattice_size)
    
    #sum of nearest neighbours
    nn_sum = sum([array[left[0], left[1]],
                  array[right[0], right[1]],
                  array[top[0], top[1]],
                  array[bottom[0], bottom[1]],
                  array[top_left[0], top_left[1]],
                  array[top_right[0], top_right[1]],
                  array[bottom_left[0], bottom_left[1]],
                  array[bottom_right[0], bottom_right[1]]
                  ])
    return nn_sum


def array_update(array, lattice_size):
    """
    update array based on game of life rules
    return number of active sites
    
    alive cell check
     < 2 alive neighbours = death
      2 or 3 alive neighbours = life
      > 3 alive neighbours = death
      
    dead cell check
     3 alive neighbours = life
    """
    #copy to new array, need to have old one to ensure iteration works
    new_array = np.copy(array)
    #start tally for active sites
    a_sites = 0
    #scan across entire array
    for i in range(lattice_size):
        for j in range(lattice_size):
            nn_count = nn_check(array, lattice_size, i, j)
            
            #if dead and three alive neighbours
            if ((array[i, j] == False) and (nn_count == 3)):
                #bring to life
                new_array[i, j] = True
                a_sites += 1
            #if alive
            elif ((array[i, j] == True)):
                
                #and 2 or 3 neighbours
                if (nn_count == 2 or nn_count == 3):
                    #stay alive
                    continue;
                else: #else death
                    new_array[i, j] = False
                    a_sites += 1
    #return new array and number of active sites       
    return new_array, a_sites

#initialises and iterates over the array, updating via above function
def gol_sim_run(lattice_size, iterations, init_conditions, mode):
    #initial conditions
    # 0 - random
    # 1 - oscillator
    # 2 - glider
    # 3 - absorber
    
    #define array
    if init_conditions == 0:
        print("Running random simulation...")
        array = gol_array_rand(lattice_size)
    elif init_conditions == 1:
        print("Running oscillator simulation...")
        array = gol_array_osc2(lattice_size)
    elif init_conditions == 2:
        print("Running glider simulation...")
        array = gol_array_glider(lattice_size)
    elif init_conditions == 3:
        print("Running absorption simulation...")
        array = gol_array_beehive(lattice_size)
       
    #visualising
    if mode == 0:
        #iterate over array
        for i in range(iterations):
            n = 1
            #plot every nth
            if (i%n == 0):
                plt.cla()
                im = plt.imshow(array, animated=True, cmap='hot')
                plt.draw()
                plt.pause(0.05)
                
            array, n_a_sites = array_update(array, lattice_size)
        
        #return 0 to be consistent for equilibrium testing component
        return 0
    
    #finding equilibrium
    elif mode == 1:
        print("Searching for equilibrium...")
        i = 0
        eq_val  = 0
        a_sites = 0
        #loop until equilibrium is reached for 10 updates
        while (eq_val < 10):
            array, n_a_sites = array_update(array, lattice_size)
            if n_a_sites == a_sites:
                eq_val += 1
            else:
                eq_val = 0
            a_sites = n_a_sites
            i += 1
        #return number of iterations until equilibrium is reached
        print("Equilibrium reached at: {}".format(i))
        return i
    
    #glider calculation - produce plots of glider path and write to textfile
    elif mode == 2:
        print("Glider speed calculations...")
        
        com_list = []
        iter_list = []
        for i in range(iterations):
            #update array
            array, n_a_sites = array_update(array, lattice_size)
            
            if (i>70 and i%10 == 0):
                print("Sweep {}/{}".format(i, iterations))
                 
                
                #screendoor scanning to check not going across boundary
                
                # x_min
                check = False
                p = 0
                while (check==False):
                    #if a living cell in column p, change check to True
                    if True in array[:, p]:
                        check = True
                        x_min = p
                    p+= 1
                
                # x_max
                # start from last column and scan backwards
                check = False
                p = lattice_size -1
                
                while (check==False):
                    #if a living cell in column p, change check to True
                    if True in array[:, p]:
                        check = True
                        x_max = p
                    p-= 1
                
                # y_min
                check = False
                p = 0
                
                while (check==False):
                     #if a living cell in row p, change check to True
                    if True in array[:, p]:
                        check = True
                        y_min = p
                    p+= 1
                
                # y_max
                # start from last row and scan backwards
                check = False
                p = lattice_size -1
                
                while (check==False):
                    #if a living cell in row p, change check to True
                    if True in array[:, p]:
                        check = True
                        y_max = p
                    p-= 1
                
                # if x_max - x_min > lattice_size/2 assume boundary crossing and ignore (and same for y)
                if (x_max - x_min > lattice_size/2) or (y_max - y_min > lattice_size/2):
                    continue;
                #if not boundary crossing, calculate COM
                else:
                    x_numer = 0
                    x_denom = 0
                    y_numer = 0
                    y_denom = 0
                    for j in range(lattice_size):
                        for k in range(lattice_size):
                            #collect sum
                            x_numer += j * array[j, k]
                            x_denom += array[j, k]
                            
                            y_numer += k * array[j, k]
                            y_denom += array[j, k]
                    
                    #after simulation, divide and collect
                    x_mass = (x_numer/x_denom)
                    y_mass = (y_numer/y_denom)
                    iter_list.append(i)
                    com_list.append([x_mass, y_mass])
                        
        #plot COM XY plot            
        com_list = np.array(com_list)
        plt.scatter(com_list[:, 0], com_list[:, 1], marker='x')
        plt.xlabel("X position")
        plt.ylabel("Y position")
        plt.title("Flight of glider across XY coords, each point taken every 10 iterations")
        plt.savefig("glider_path1.png")
        plt.show()
        
        #plot COM x plot
        plt.scatter(iter_list, com_list[:,0], marker='x')
        plt.xlabel("Iteration")
        plt.ylabel("X position")
        plt.title("Flight of glider across X coords, each point taken every 10 iterations")
        plt.savefig("glider_pathX1.png")
        plt.show()
        
        #plot COM y plot
        plt.scatter(iter_list, com_list[:, 1], marker='x')
        plt.xlabel("Iteration")
        plt.ylabel("Y position")
        plt.title("Flight of glider across Y coords, each point taken every 10 iterations")
        plt.savefig("glider_pathY1.png")
        plt.show()
        
        #write to file
        pos_write(com_list, "com_list1.txt")
        pos_write(iter_list, "iter_list1.txt")
        
        return 0
    
  # used in scripts that import these functions  
def pos_write(data, file_name):
    with open(file_name, "w") as f:
        for i in range(len(data)):
            pos = str(data[i])
            pos = pos.strip("[]")
            pos = pos.replace(",", "")
            f.write(pos + "\n")
            
def read_file(file_name):
    with open(file_name) as f:
        contents = f.readlines()
        
    if (len(contents) > 1):
        print("File read of length: " + str(len(contents)))
    else:
        print("File length is too short to process (please include more positions)")
    
    return contents

if __name__ == "__main__":
    if len(sys.argv) == 5:
        #run code, force as integers
        gol_sim_run(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
    else:
        print("\nScript takes exactly 4 arguments, " + str(len(sys.argv)-1) + " were given")
        print("\nPlease input:\n\n LATTICE SIZE\n\n ITERATIONS\n\n INITIAL CONDITIONS\n 0 - Random\n 1 - Oscillator\n 2 - Glider\n 3 - Absorption\n\n MODE\n 0 - Visualisation\n 1 - Equilibrium Locating\n 2 - Glider calculations")
                
    