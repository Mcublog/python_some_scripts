import os
import shutil
import sys
import subprocess

func_opto_path = 'C:\Project\Atmel\hb_firmware_func_opto\SAM4'
func_opto_name = 'Sensor (SAM4SD16C).bin'
board_list = ['4', '4L']


def clear(version):
    if os.path.isdir(version):
        shutil.rmtree(version)


def main():
    ver = ''
    if len(sys.argv) != 1:
        ver = sys.argv[1]

    prog = False
    copy = False
    if 'p' in sys.argv:
        prog = True
    if 'c' in sys.argv:
        copy = True
    if ver not in board_list:
        return print('Version unknown: '+ ver)

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


if __name__ == '__main__':
    main()
