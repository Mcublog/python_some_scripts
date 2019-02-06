import os
import subprocess
import sys


bossa_path: str = 'C:\\Program Files\\BOSSA\\bossac.exe'
func_path: str = '"' + os.getcwd() + '\\SAM4\\Sensor (SAM4SD16C).bin"'
print(bossa_path)
print(func_path)
args = [bossa_path + ' -e -w -b -p COM4 ' + func_path]
for i in range(2):
    subprocess.call([args])    