import os
import shutil
import sys


# Default paths
path = {
    'local': 'C:\Project\GuiDemoUart',
    'remote': '\\\Healbeserver\программное обеспечение\GUI Demo\GUI Demo Opto'
    }
    

def find_demo(path):
    for file in os.scandir(path):
        if '.exe' in file.name:
            print('Find .exe: ' + file.name)
            return file.name


def main():
    if len(sys.argv) > 2:
        path['local'] = sys.argv[1]
        path['remote'] = sys.argv[2]

    demo_name: str = find_demo(os.getcwd())# Find src name
    if not demo_name:
        return print('local.exe not found')
    remote: str = find_demo(path['remote'])# Find dst name

    # Check dst file
    if not remote:
        print('remote.exe not found')

    if remote == demo_name:
        os.remove(path['remote'] + '\\' + remote)
        return print('remote.exe == local.exe')

    shutil.copy(demo_name, path['local'], follow_symlinks=True)
    print('Remove: ' + remote)
    os.remove(path['remote'] + '\\' + remote)

    print('Copy to: ' + path['remote'])
    shutil.copy(demo_name, path['remote'], follow_symlinks=True)
    print('Rename: ' + demo_name + ' to ' + remote)
    os.rename(path['remote'] + '\\' + demo_name, path['remote'] + '\\' + remote)
    print('Copy success')


if __name__ == '__main__':
    main()
