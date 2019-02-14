import os
import shutil
import subprocess
import sys
import getopt


def usage():
    print("""Usage: %s [-h] [-p port]
    -h          This help
    -p          Bossa port
    """ % sys.argv[0])


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'p:', ["port="])
    except getopt.GetoptError as err:
        usage() # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        sys.exit(2)

    port: str = ''
    for o, a in opts:
        if o in ("-p", "--port"):
            port = a
        else:
            return print("Undefined param" + o)

    # Find digit in port name
    if not any(map(str.isdigit, port)):
        # Default port
        port = 'COM4'
        
    bossa_path: str = 'C:\\Program Files\\BOSSA\\bossac.exe'
    func_path: str = '"' + os.getcwd() + '\\SAM4\\Sensor (SAM4SD16C).bin"'
    print(bossa_path)
    print(func_path)
    args = [bossa_path + ' -e -w -b -p '+ port + ' ' + func_path]
    for i in range(2):
        subprocess.call([args])


if __name__ == '__main__':
    main()
 
