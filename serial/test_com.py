import serial
import time


ser = serial.Serial()
ser.baudrate = 1500000
ser.port = 'COM18'
ser.open()
print('Port: ' + ser.port + ' open')

cmd_list = {
    'sensor_state'  :   '<#0A00',
    'set_time'      :   '<#000C820001000000',
    'sensor_info'   :   '<#0100',
    'long_cmd'      :   '<#0150250918200C82804367000000000000000000000000000040B9466859302A0000000000006500000000',
    'heart_rate'    :   '<#1200'
    }


cmd = 'heart_rate'

print('send data: ' + cmd_list[cmd])
ser.write(cmd_list[cmd].encode())

#chunk: int = int(round(len(cmd_list[cmd])/6))
#print('chunk num: ' + str(chunk))
#for i in range(chunk):
#    c = cmd_list[cmd][i*6:(i*6)+6]
#    print('send data: ' + c)
#    ser.write(c.encode())
#    time.sleep(.04)

for i in range(5):  # Waiting 500 ms maximum
    if ser.in_waiting:
        break
    time.sleep(.1)  # Waiting 100 ms

if ser.in_waiting == 0:
    print('no data received')
    ser.close()
    raise SystemExit(0)

s : str ='data received: '
while ser.in_waiting:
    try:
        s += ser.read().decode('utf-8')
    except:
        print('not hex')

print(s)

print('Port: ' + ser.port + ' close')
ser.close()
