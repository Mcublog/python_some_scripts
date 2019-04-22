import os
from ctypes import *

class time_stamp_t(Structure):
    _fields_ = [
        ("time", c_uint),
        ("t_ms", c_ushort),
        ("day",  c_ushort),
        ("date", c_ushort),
    ]


print('Start prog...')
path = os.getcwd() + '\\Ctypes\\Debug\\Cpython_test.dll'
clib = CDLL(path)

for i in range(5):
    cnt = clib.test_function()
    print('cnt: ' + str(cnt))
    
time = time_stamp_t()
clib.test_function_struct(byref(time))
t_ms = time.t_ms

print(t_ms)



print('End')