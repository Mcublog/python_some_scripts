import serial,time

from xcrc32 import xcrc32

  
buf = b'[\x23\x00\x00\x00]' # Form lenght
buf += b'[GET_NAME][string][0]' # Form body

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
ser.close()