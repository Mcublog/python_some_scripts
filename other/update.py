import os
import shutil
import sys
import subprocess
import getopt


def clear(version):
    if os.path.isdir(version):
        shutil.rmtree(version)


def main():  
    # Defaults
    func_opto_path = 'C:\Project\Atmel\hb_firmware_func_opto\SAM4'
    func_opto_name = 'Sensor (SAM4SD16C).bin'
    board_list = ['4', '4L']    
    ver = ''
    prog = False
    copy = False
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'p:n:b:uf', ["path=", "name=", "board="])
    except getopt.GetoptError as err:
        usage() # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        sys.exit(2)
    
    for o, a in opts:
        if o == "-f":
            prog = True
        elif o == "-u":
            copy = True
        elif o in ("-p", "--path"):
            func_opto_path = a
        elif o in ("-n", "--name"):
            func_opto_name = a 
        elif o in ("-b", "--board"):
            ver = a
        else:
            return print("Undefined param" + o)

    if ver not in board_list:
        print('Version unknown: '+ ver)
        return usage()

    print('Version board: '+ ver)
    
    if copy:
        clear(ver)
        os.mkdir(ver)
        shutil.copy(func_opto_path + '\\' + func_opto_name, os.getcwd() + '\\' + ver, follow_symlinks=True)
        print('Board version '+ ver + ' file update')

    if prog:
        file_path = '"'+ os.getcwd() + '\\' + ver + '\\' + func_opto_name + '"'
        args = ["bossa\\bossac.exe -e -w -v -b -p COM4 " + file_path]
        subprocess.call([args])
        try:
            subprocess.call(args)
            print('Board version '+ ver + 'firmware update')
        except:
            print('Bossa error')

    os.system("pause")

def usage():
    print("""Usage: %s [-h] [-p path] [-n name] [-b board] [-f] [-u]
    -h          This help
    -p          Path to opto firmware file (C:\Project\Atmel\hb_firmware_func_opto\SAM4)
    -n          Name of opto firmware (Sensor (SAM4SD16C).bin)
    -b          Board version (4, 4L)
    -f          Prog board with bossa
    -u          Just copy files in work directory
    """ % sys.argv[0])


if __name__ == '__main__':
    main()
