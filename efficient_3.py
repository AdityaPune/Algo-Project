# import modules     

import sys
import os
import gc
import psutil
import numpy as np
import copy
import time

# set alpha and delta     

ALPHA = {'A' : {'A' : 0,
                     'C' : 110,
                     'G' : 48,
                     'T' : 94},
            'C' : {'A' : 110,
                    'C' : 0,
                    'G' : 118,
                    'T' : 48},
            'G' : {'A' : 48,
                    'C' : 118,
                    'G' : 0,
                    'T' : 110},
            'T' : {'A' : 94,
                    'C' : 48, 
                    'G' : 110, 
                    'T' : 0}}

DELTA = 30

# function: read input file     

def readInputFile(filename):
    with open(filename) as f:
        string1 = None
        string2 = None
        base_temp_string = None
        for line in f:
            tempstring = line.rstrip()
            if not tempstring.isdecimal():
                string1 = base_temp_string
                base_temp_string = tempstring
                
            if tempstring.isdecimal():
                insert_index = int(tempstring)
                insert_index+=1
                base_temp_string = base_temp_string[:insert_index] + base_temp_string + base_temp_string[insert_index:]
        
        if string2 is None:
            string2 = base_temp_string

    return string1, string2

def alignment(string1, string2):
    n, m = len(string1), len(string2)
    opt_array = []
    for i in range(n+1):
        opt_array.append([0]*(m+1))
        opt_array[i][0] = DELTA*i
    for j in range(m+1):
        opt_array[0][j] = DELTA*j
    for i in range(1, n+1):
        for j in range(1, m+1):
            opt_array[i][j] = min(opt_array[i-1][j-1] + ALPHA[string1[i-1]][string2[j-1]], opt_array[i][j-1] + DELTA, opt_array[i-1][j] + DELTA)
    align1 = ""
    align2 = ""
    i, j = n, m
    while i and j:
        if opt_array[i][j] == opt_array[i-1][j-1] + ALPHA[string1[i-1]][string2[j-1]]:
            align1 = string1[i-1] + align1
            align2 = string2[j-1] + align2
            i -= 1
            j -= 1
        elif opt_array[i][j] == opt_array[i-1][j] + DELTA:
            align1 = string1[i-1] + align1
            align2 = '_' + align2
            i -= 1
        elif opt_array[i][j] == opt_array[i][j-1] + DELTA:
            align1 = '_' + align1
            align2 = string2[j-1] + align2
            j -= 1
    while i:
        align1 = string1[i-1] + align1
        align2 = '_' + align2
        i -= 1
    while j:
        align1 = '_' + align1
        align2 = string2[j-1] + align2
        j -= 1
    return [align1, align2, opt_array[n][m]]

def space_efficient_alignment(string1, string2):
    n, m = len(string1), len(string2)
    opt_array = []
    opt_array.append([0]*(m+1))
    opt_array.append([0]*(m+1))
    for j in range(m+1):
        opt_array[0][j] = DELTA*j
    for i in range(1, n+1):
        opt_array[1][0] = opt_array[0][0] + DELTA
        for j in range(1, m+1):
            opt_array[1][j] = min(opt_array[0][j-1] + ALPHA[string1[i-1]][string2[j-1]], opt_array[0][j] + DELTA, opt_array[1][j-1] + DELTA)
        opt_array[0] = copy.deepcopy(opt_array[1])
    return opt_array[0] 

def backward_space_efficient_alignment(string1, string2):
    n, m = len(string1), len(string2)
    opt_array = []
    opt_array.append([0]*(m+1))
    opt_array.append([0]*(m+1))
    for j in range(m+1):
        opt_array[0][j] = DELTA*j
    for i in range(1, n+1):
        opt_array[1][0] = opt_array[0][0] + DELTA
        for j in range(1, m+1):
            opt_array[1][j] = min(opt_array[0][j-1] + ALPHA[string1[n-i]][string2[m-j]], opt_array[0][j] + DELTA, opt_array[1][j-1] + DELTA)
        opt_array[0] = copy.deepcopy(opt_array[1])
    return opt_array[0]

def divide_and_conquer(string1, string2):
    n, m = len(string1), len(string2)
    if n<2 or m<2:
        return alignment(string1, string2)
    else:
        f, g = space_efficient_alignment(string1[:int(n/2)], string2), backward_space_efficient_alignment(string1[int(n/2):], string2)
        partition = [f[j] + g[m-j] for j in range(m+1)]
        q = partition.index(min(partition))
        del f, g, partition
        gc.collect()
        left = divide_and_conquer(string1[:int(n/2)], string2[:q])
        right = divide_and_conquer(string1[int(n/2):], string2[q:])
        return [left[i] + right[i] for i in range(3)]


# MAIN Function call        

if __name__=="__main__":
    # def myfunc():
    proc = psutil.Process(os.getpid())
    start = time.process_time()
    string1, string2 = readInputFile(sys.argv[1])
    write_log_file = False
    result = divide_and_conquer(string1, string2)
    end = time.process_time()
    mem = proc.memory_info().rss
    memory_in_kb = mem / 1024

    f = open("output-eff.txt", 'w')
    f.write(result[0][:50] + " " + result[0][-50:] + "\n")
    f.write(result[1][:50] + " " + result[1][-50:] + "\n")
    f.write(str(float((result[2]))) + "\n")
    f.write(str(end-start) + "\n")
    f.write(str(memory_in_kb))
    f.close()

    if write_log_file:
        with open('plotlogs3.txt', 'a') as log_file:
            log_file.write(str(len(string1) * len(string2)) +', '+ str(end - start) +', '+ str(memory_in_kb)+'\n')
