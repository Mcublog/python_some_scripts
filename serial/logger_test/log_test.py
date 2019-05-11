import serial, time
import time, datetime
import re

from xcrc32 import xcrc32


CMD_LENGHT_ADD = 14

body = b'[GET_0][string][0]'
body_len = len(body) + CMD_LENGHT_ADD

# Form CMD
buf = b'[' + body_len.to_bytes(4, byteorder='little') + b']' 
buf += body

# Added crc32 to buf
crc = xcrc32 (buf, len(buf)) 
buf+=b'['
buf+= crc.to_bytes(4, byteorder='little')
buf+=b']\r\n'
print(buf)

ser = serial.Serial()

ser.baudrate = 115000
ser.port = 'COM3'

ser.open()
print('Port: ' + ser.port + ' open')
ser.write(buf)

for i in range(5):  # Waiting 500 ms maximum
    if ser.in_waiting:
        break
    time.sleep(.1)  # Waiting 100 ms

if ser.in_waiting == 0:
    print('no data received')
    ser.close()
    raise SystemExit(0)

s = b''
while ser.in_waiting:
    try:
        s += ser.readline()
    except:
        print('not hex')
print(s)

test_buf = s[:-8]
print(test_buf)
crc_cnt = xcrc32 (test_buf, len(test_buf))
crc = s[-7:-3]
crc = int.from_bytes(crc, byteorder='little')
if (crc == crc_cnt):
    print('Crc correct:' + hex(crc) + ':' + hex(crc_cnt))


try:
    s = s[6:]
    s = s.decode('utf-8', errors = 'ignore')
except:
    print('not hex at ' + str(datetime.datetime.now().ctime()))
    s = ''

print('string:' + s)

param = re.findall(r'[\[]\w*[\]]', s)
print(param)

ser.close()