import os
from ctypes import *

print('Start prog...')
path = os.getcwd() + '\\Ctypes\\Debug\\Cpython_test.dll'
clib = CDLL(path)

for i in range(5):
    cnt = clib.test_function()
    print('cnt: ' + str(cnt))

print('End')