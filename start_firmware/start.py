import os
import shutil
import subprocess
import sys

#base_path: str = 'C:\Project\Atmel\hb_firmware_base\SAM4'
#func_path: str = 'C:\Project\Atmel\hb_firmware_func\SAM4'

base_name: str = 'Sensor_base.bin'
func_orig_name: str = 'Sensor (SAM4SD16C).bin'

func_name: str = 'Func.bin'
work_dir: str = 'Files'

com_port = 'COM4'

def clear():
    if os.path.isdir(work_dir):
        shutil.rmtree(work_dir)


def file_not_found(name: str):
    print()
    print('File: ' + name + ' not found')

   
def usage():
    print()
    print('=================Help================')
    print()
    print('start.py <path to base> <path to func> <bossa com port>')
    print()
    print('for example:')
    print('start.py C:\Project\Atmel\hb_firmware_base\SAM4 C:\Project\Atmel\hb_firmware_func\SAM4')
    print()
    print('Base file should be called: ' + base_name)
    print('Func file should be called: ' + func_orig_name)
    print()
    print('Bossa COM Port: ' + com_port)
    print('=================Help================')
    print()
    os.system("pause")


def main():
    if len(sys.argv) < 3:
        return usage()
    base_path = sys.argv[1]
    func_path = sys.argv[2]
    if sys.argv[3]:
        base_name = sys.argv[3]
        print('Base name: ' + base_name)
    if sys.argv[4]:
        func_orig_name = sys.argv[4]
        print('Base name: ' + func_orig_name)
    if sys.argv[5]:
        com_port = sys.argv[5]
    print()
    print('Processing.......')
    print('Base path: ' + base_path)
    print('Func path: ' + func_path + '\r\n')
    print('Bossa COM port: ' + com_port)
    
    # Clean and Make dir
    clear()
    work_path: str = os.getcwd() + '\\' + work_dir
    os.mkdir(work_path, 0)
    
    # Copy Sensor_base.bin
    try:
        shutil.copy(base_path + r'\\' + base_name, work_path, follow_symlinks=True)
    except FileNotFoundError:
        file_not_found(base_name)
        return usage()
    
    # Copy Sensor (SAM4SD16C).bin
    try:
        shutil.copy(func_path + r'\\' + func_orig_name, work_path, follow_symlinks=True)
    except FileNotFoundError:
        file_not_found(func_orig_name)
        return usage()

    # Rename files, start cmd, prog firmware and clear
    os.rename(work_dir + '\\' + func_orig_name, work_dir + '\\' + func_name)
    subprocess.call(['mk_img_func.cmd'])
    print("firmware.img done...\n")
    
    img_path = '"Files\\Sensor_base.bin"'
    args = ["bossa\\bossac.exe -e -w -v -b -p " + com_port + ' ' + img_path]
    for i in range(2):
        if (i == 1):
            args.append(' -R')
        if subprocess.call([args]) != 0:
            print('Firmware flash fail...')
            break
    clear()

    print()
    print('Complete...')
    os.system("pause")


if __name__ == '__main__':
    main()
