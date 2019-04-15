import serial
import time, datetime
import os, sys

ser = serial.Serial()
ser.baudrate = 250000
ser.port = 'COM6'

try:
    ser.open()
except:
    print('Port not opened: ' + ser.port)
    sys.exit(0)

print('Port: ' + ser.port + ' is open')

s : str =''
stop = 0

log_name = 'battery '+ str(datetime.datetime.now().ctime()) +'.txt'
log_name = log_name.replace(':', '_')

div = 0

while(1):
    bytes = b''
    while ser.in_waiting:
        bytes += ser.read()

    for byte in bytes:
        if byte == 0x00 or byte >= 128:
            print(byte)
            stop = 1
            print('stop = ' + str(stop))
            break
            
    if (stop):
        break
        
    if (bytes):
        try:
            print(bytes)
            s += bytes.decode('utf-8', errors = 'strict')
        except:
            print('not hex at ' + print('wait ' + str(datetime.datetime.now().ctime())))
            break
            
    # Save to file
    if s != '':
        file_exist = 1;
        try:
            f = open(os.getcwd() + '\\' +log_name, 'r')
        except:
            f = open(os.getcwd() + '\\' +log_name, 'w') # Create file
            file_exist = 0

        if file_exist:
            f = open(os.getcwd() + '\\' +log_name, 'a')
    
        f.write(s)
        f.close()
        s = ''
    
    div +=1
    if div == 60:
        div = 0
        print('Working: ' + str(str(datetime.datetime.now().ctime())))
    if stop:
        print('stop = ' + str(stop))
        break
    time.sleep(1)

print('Port: ' + ser.port + ' close')
ser.close()