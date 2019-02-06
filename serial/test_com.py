import serial
import time


ser = serial.Serial()
ser.baudrate = 250000
ser.port = 'COM14'
ser.open()
print('Port: ' + ser.port + ' open')

cmd = '<#0150250918200C82804367000000000000000000000000000040B9466859302A0000000000006500000000'
#cmd = '<#8568010000004B000000AA0000000D0000000B000000A2070000780000005000000046000000040000004B0000004600000000000000'

chunk: int = int(round(len(cmd)/6))
print('chunk num: ' + str(chunk))

for i in range(chunk):
    c = cmd[i*6:(i*6)+6]
    print('send data: ' + c)
    ser.write(c.encode())
    time.sleep(.04)

for i in range(5):  # Waiting 500 ms maximum
    if ser.in_waiting:
        break
    time.sleep(.1)  # Waiting 100 ms

if ser.in_waiting == 0:
    print('No data received')

s : str =''
while ser.in_waiting:
    s += ser.read().decode('utf-8')

print(s)

print('Port: ' + ser.port + ' close')
ser.close()
