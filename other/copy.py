import os
import shutil
import sys, getopt


def usage():
    print("""Usage: %s [-h] [-l local] [-r remote]
    -h          This help, !!There can be only one .exe file in a GUI Demo directory.
    -l          Local path to GUI Demo
    -r          Remote path to GUI Demo
    """ % sys.argv[0])

# Default paths
path = {
    'local': 'C:\Project\GuiDemoUart',
    'remote': '\\\Healbeserver\тестирование\GUI Demo\GUI Demo Opto'
    }
    

def find_demo(path):
    for file in os.scandir(path):
        print(file)
        if '.exe' in file.name:    
            if 'GUI' in file.name:
                print('Find .exe: ' + file.name)
                return file.name
            elif 'guidemo' in file.name:
                print('Find .exe: ' + file.name)
                return file.name


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hl:r:', ["local=", "remote="])
    except getopt.GetoptError as err:
        usage() # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        sys.exit(2)            
    for o, a in opts:
        if o in ('-h'):
            usage()
            return
        elif o in ("-l", "--local"):
            path['local'] = a
            print(path['local'])
        elif o in ('-r',"--remote"):
            path['remote'] = a
            print(path['remote'])
        else:
            return print("Undefined param" + o)

    demo_name: str = find_demo(os.getcwd())# Find src name
    if not demo_name:
        return print('local.exe not found')
    try:
        remote: str = find_demo(path['remote'])# Find dst name
    except:
        remote = 'not found'

    shutil.copy(demo_name, path['local'], follow_symlinks=True)


    # Check dst file
    if remote != 'not found':
        print('Remove: ' + remote)
        os.remove(path['remote'] + '\\' + remote)    
        if not remote:
            print('remote.exe not found')
        if remote == demo_name:
            os.remove(path['remote'] + '\\' + remote)
            return print('remote.exe == local.exe')

        shutil.copy(demo_name, path['remote'], follow_symlinks=True)
        print('Copy to: ' + path['remote'])
        os.rename(path['remote'] + '\\' + demo_name, path['remote'] + '\\' + remote)
        print('Rename: ' + demo_name + ' to ' + remote)

    print('Copy success')


if __name__ == '__main__':
    main()
