import os, psutil
import numpy as np
import time
import sys
import collections


COSTS = {'A' : {'A' : 0,
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


def readInputFile(filename):
    with open(filename) as f:
        s1 = ""
        s2 = ""
        curr = ""
        for line in f:
            temp = line.rstrip()
            if not temp.isdecimal():
                s1 = curr
                curr = temp              
            else:
                index = int(temp) + 1
                curr = curr[:index]+curr+curr[index:]

    s2 = curr

    
    return s1, s2

def align(string1, string2):
    def reconstruct(string1, string2, opt_array):

        opt_array = np.vstack([np.ones((1,opt_array.shape[1])) * -np.inf, opt_array])
        opt_array = np.hstack([np.ones((opt_array.shape[0],1)) * -np.inf, opt_array])

        ans1 = collections.deque()
        ans2 = collections.deque()

        i, j = opt_array.shape
        i-=1
        j-=1

        while True:
            if i == 1 and j == 1:
                break
            if opt_array[i][j] == opt_array[i-1][j-1] + COSTS[string1[i-2]][string2[j-2]]:
                ans1.appendleft(string1[i-2])
                ans2.appendleft(string2[j-2])
                i = i - 1
                j = j - 1
            
            elif opt_array[i][j] == opt_array[i][j-1] + DELTA:
                ans1.appendleft('_')
                ans2.appendleft(string2[j-2])
                j = j - 1
            
            elif opt_array[i][j] == opt_array[i-1][j] + DELTA:
                ans1.appendleft(string1[i-2])
                ans2.appendleft('_')
                i = i - 1

        return ''.join(ans1), ''.join(ans2)
    
    m = len(string1)
    n = len(string2)

    # opt_array = [[0 for _ in range(m+1)] for _ in range(n+1)]

    opt_array = np.zeros((m+1, n+1))

    #INITIALIZATION
    opt_array[0,:] = np.arange(n+1)*DELTA
    opt_array[:,0] = np.arange(m+1)*DELTA

    #ITERATION
    for i in range(1, m+1):
        for j in range(1, n+1):
            opt_array[i][j] = min(opt_array[i - 1][j - 1] + COSTS[string1[i-1]][string2[j-1]],
                                opt_array[i - 1][j] + DELTA ,
                                opt_array[i][j - 1] + DELTA )
    
    align1, align2 = reconstruct(string1, string2, opt_array)
    return opt_array, opt_array[-1][-1], align1, align2

if __name__ == '__main__':

    proc = psutil.Process(os.getpid())
    start = time.process_time()
    input_path = sys.argv[1]
    string1, string2 = readInputFile(input_path)
    opt, opt_cost, x, y = align(string1, string2)
    end = time.process_time()
    write_log_file = False
    mem = proc.memory_info().rss
    memmory_in_kb = mem / 1024

    with open('output1.txt', 'w') as f:
        f.write(str(x[:50] + ' ' + x[-50:])+'\n')
        f.write(str(y[:50] + ' ' + y[-50:])+'\n')
        f.write(str(opt_cost)+'\n')
        f.write(str(end - start)+'\n')
        f.write(str(memmory_in_kb))
        
    if write_log_file:
        with open('plotlogs2.txt', 'a') as f2:
            f2.write(str(len(string1) * len(string2)) +', '+ str(end - start) +', '+ str(memmory_in_kb)+'\n')


