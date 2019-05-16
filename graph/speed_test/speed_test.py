import matplotlib.pyplot as plt
import os, sys

import speed_test_parse as stp

f = open(os.getcwd() + '\\test\\4096.txt', 'r')
data = f.read()
numbers = stp.get_param(data, 'block num')
speeds = stp.get_param(data, 'speed')

print(speeds)
print(numbers)
f.close()



