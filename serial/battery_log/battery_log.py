import serial
import time, datetime
import os, sys, getopt
import msvcrt

def usage():
    print("""Usage: %s [-h] [-p port]
    -h          This help
    -p          COM port number
    """ % sys.argv[0])

def battery_get_charge(s):
    # battery: [56 %, 3794 mV, limiter 52 %]
    if 'battery: [' in s:
        if '%' in s:
            return s[(s.find('[') + 1) : (s.find('%') + 1)]
    return ''


def battery_logging(com_name = 'COM20'):
    ser = serial.Serial()
    ser.baudrate = 250000
    ser.port = com_name

    try:
        ser.open()
    except:
        print('Port not opened: ' + ser.port)
        input("Press ENTER to quit")
        sys.exit(0)

    print('Port: ' + ser.port + ' is open')
    print("Press 'q' to exit")

    s =''
    stop = 0
    charge = ''
    div = 0
    
    log_name = 'battery '+ str(datetime.datetime.now().ctime()) +'.txt'
    log_name = log_name.replace(':', '_')
    
    print('Log will be saved to a file.: ' + log_name)
    while(1):
        bytes = b''
        while ser.in_waiting:
            bytes += ser.read()
            
        for byte in bytes:
            if byte == 0x00 or byte == 255:
                print('Garbage byte detected: ' + str(byte))
                bytes = b''
                stop = 1
                break
        
        if (bytes):
            try:
                s += bytes.decode('utf-8', errors = 'strict')
            except:
                # print('not hex at ' + str(datetime.datetime.now().ctime()))
                s = ''
        if "IMP METER:" in s:
            s = ''
        if "<<START MEASURING IMPEDANCE" in s:
            s = ''
            
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
                
            if battery_get_charge(s):
                charge = battery_get_charge(s)
            f.write('---------------- ' + str(datetime.datetime.now().ctime()) + ' ---------------- ')
            f.write(s)
            f.write('-----------------------------------------\r\n')
            f.close()
            s = ''

        div += 1
        # print a log every 10 minutes
        if div == 60 * 10:
            div = 0
            if charge:
                print('Current charge: ' + charge + ' at ' + str(str(datetime.datetime.now().ctime())))
            else:
                print('Still working: ' + str(str(datetime.datetime.now().ctime())))
            
        if stop:
            break
        else:
            time.sleep(1)
        
        if msvcrt.kbhit():
            char =msvcrt.getch()
            # print(char)
            if char == b'q':
                print("you pressed " + str(char) + "so now i will stop logging")
                break

    print('Port: ' + ser.port + ' close')
    ser.close()
    print("Stop logging")
    input("Press ENTER to quit")

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hp:', ["port="])
    except getopt.GetoptError as err:
        usage() # print help information and exit:
        sys.exit(2)

    com_port =''
    for o, a in opts:
        if o in ('-h'):
            usage()
            return
        elif o in ("-p", "--port"):
            com_port = a
            # print(path['local'])
        else:
            return print("Undefined param" + o)
    if com_port:
        battery_logging(com_port)
    else:
        battery_logging()

if __name__ == '__main__':
    main()
