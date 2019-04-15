import serial
import time, datetime
import os, sys
import msvcrt

    
def battery_loging():
    ser = serial.Serial()
    ser.baudrate = 250000
    ser.port = 'COM6'

    try:
        ser.open()
    except:
        print('Port not opened: ' + ser.port)
        sys.exit(0)

    print('Port: ' + ser.port + ' is open')
    print("Press 'q' to exit")
    
    
    s : str =''
    stop = 0

    log_name = 'battery '+ str(datetime.datetime.now().ctime()) +'.txt'
    log_name = log_name.replace(':', '_')

    div = 0
    print('Log will be saved to a file.: ' + log_name)
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
                s += bytes.decode('utf-8', errors = 'strict')
            except:
                print('not hex at ' + print('wait ' + str(datetime.datetime.now().ctime())))
            
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
    
        div += 1
        if div == 60:
            div = 0
            print('Still working: ' + str(str(datetime.datetime.now().ctime())))
        if stop:
            print('Stop at ' + + str(str(datetime.datetime.now().ctime())))
            break
        time.sleep(1)
        
        if msvcrt.kbhit():
            char =msvcrt.getch()
            # print(char)
            if char == b'q':
                print("you pressed " + str(char) + "so now i will stop logging")
                break

    print('Port: ' + ser.port + ' close')
    ser.close()

def main():
    battery_loging()

if __name__ == '__main__':
    main()