import matplotlib.pyplot as plt
import math, os
import numpy as np
import sys, shutil
import re

def get_param(data, param):

    exp = r''
    if ('speed' == param):
        exp = r'[^Tt]+' + param + ': ' + '(\d+.\d+)'
    elif ('block num' == param):
        exp = r'[^Tt]+' + param + ': ' + '(\d+)'
    else:
        exp = r'[^Tt]+' + param + ': ' + '(\d+)'
        
    params = re.findall(exp, data)

    # print(params)
    # print('len: ' + str(len(params)))
    return params

def main():
    f = open(os.getcwd() + '\\test\\test_data.txt', 'r')
    data = f.read()
    f.close()
    
    start_times = get_param(data, 'start time')
    stop_times = get_param(data, 'stop time')
    
    start = []
    stop = []
    for stt, stp in zip(start_times, stop_times):
        start.append(int(stt))
        stop.append(int(stp))
        
    print(start)
    print(stop)
        
    print(np.subtract(stop,start))
    

if __name__ == '__main__':
    main()


