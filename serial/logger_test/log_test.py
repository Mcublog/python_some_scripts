import serial, time
import time, datetime
import re
import random

from xcrc32 import xcrc32

def parse_cmd(s):
    crc_cnt = s[:-8]
    print(crc_cnt)
    crc_cnt = xcrc32 (crc_cnt, len(crc_cnt))
    
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

    param = re.findall(r'[\[](\w*|\W*|\S+)[\]]', s)
    print(param)
    return param
    
def create_cmd(body = b'[GET_NAME][string][0]'):
    CMD_LENGHT_ADD = 14 # add number service bytes
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
    return buf
    
def send_and_get_cmd(buf, port = 'COM3'):
    ser = serial.Serial()
    ser.baudrate = 115000
    ser.port = port

    try:
        ser.open()
    except:
        print("Can't open port: " + ser.port)
        raise SystemExit(0)
    
    print('Port: ' + ser.port + ' open')
    ser.write(buf)
    
    buf = b''
    for i in range(5):  # Waiting 500 ms maximum
        if ser.in_waiting:
            break
        time.sleep(.1)  # Waiting 100 ms

    if ser.in_waiting == 0:
        print('no data received')
        ser.close()
        return b''

    while ser.in_waiting:
        buf += ser.read()

    return buf

with open('app.bin', 'rb') as f:
    data = f.read()

jmp_to_fw = b'[JMP_APP][string][0]'
write_app = b'[WRITE_APP][bin][1][' + data + b']'
get_fw_ver = b'[GET_FW_VER][string][0]'

cmd = jmp_to_fw

buf = create_cmd(cmd)
data = send_and_get_cmd(buf, 'COM3')
print('RX: ' + str(data))

parse_cmd(data)