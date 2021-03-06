﻿import os
import shutil
import subprocess
import sys
import getopt


def usage():
    print("""Usage: %s [-h] [-p port] [--path] [-v]
    -h          This help
    -p          Bossa port
    -path       Path to bin
    -v          Verbouse
    """ % sys.argv[0])


def main():
    # Defaults
    func_path: str = '"' + os.getcwd() + '\\SAM4\\Sensor (SAM4SD16C).bin"'
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'p:v', ["port=", "path="])
    except getopt.GetoptError as err:
        usage() # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        sys.exit(2)

    port: str = ''
    v = 0
    for o, a in opts:
        if o in ("-p", "--port"):
            port = a
        elif o in ("--path"):
            func_path = '"' + a + '"'
        elif o in ("-v"):
            v = 1
        else:
            return print("Undefined param" + o)

    # Find digit in port name
    if not any(map(str.isdigit, port)):
        # Default port
        port = 'COM4'
        
    bossa_path: str = 'C:\\Program Files\\BOSSA\\bossac.exe'
    
    if v:
        print(bossa_path)
        print(func_path)
        
    args = [bossa_path + ' -e -w -b -p '+ port + ' ' + func_path]
    repeat = 2
    for i in range(repeat):
        if (i == repeat - 1):
            args.append(' -R')
        if subprocess.call([args]) != 0:
            print("Firmware flash fail...")
            sys.exit(2)
    

if __name__ == '__main__':
    main()
 