import matplotlib.pyplot as plt
import math, os, numpy
import sys, shutil
import re

def get_param(data, param):

    exp = r''
    if ('speed' in param):
        exp = r'[^Tt]+' + param + ': ' + '(\d+.\d+)'
    elif ('block num' in param):
        exp = r'[^Tt]+' + param + ': ' + '(\d+)'
        
    params = re.findall(exp, data)

    # print(params)
    # print('len: ' + str(len(params)))
    return params

def main():
    f = open(os.getcwd() + '\\test\\test_data.txt', 'r')
    data = f.read()
    p = get_param(data, 'block num')
    print(p)
    f.close()

if __name__ == '__main__':
    main()


