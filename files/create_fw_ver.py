import sys, os, shutil, getopt


def usage():
    print("""Usage: %s [-h] [-p] [-g]
    -h          This help, Create from last hg commit msg fw_ver[number_last_commit]
    -p          Added parameter, some like d for Debug (Optional)
    -g          Get last commit from Git
    """ % sys.argv[0])
    
def create_fw_ver_h(last_msg):
    # Create fw_ver.h
    out_path = os.getcwd()[:-len('MDK-ARM')] + 'Src\\init\\'
    fw_ver_file_name = 'fw_ver.h'
    print('Info: Create: ' + fw_ver_file_name + ' in --> ' + out_path)
    try:
        f = open(out_path + fw_ver_file_name, 'w')
    except:
        print('Error: Out path: ' + out_path + ' [NOT FIND]')
        raise SystemExit(0)
    f.write('#ifndef FW_VER_H_\n')
    f.write('#define FW_VER_H_\n\n')

    f.write('#define FW_VER "fw_v' + last_msg + '"\n\n')

    f.write('#endif /* FW_VER_H_ */\n') 
    f.close()
    print('Info: ' + fw_ver_file_name + ' [Created successfully]')
    print('Info: fw_v' + last_msg)
    
def set_fw_ver_mercurial(param = ''):
    # Find last commit msg
    path_to_hg = os.getcwd()[:-len('MDK-ARM')] + '.hg'
    print('Info: Go to --> ' + path_to_hg)
    last_msg = ''
    try:
        for file_name in os.listdir(path_to_hg):  # for each file in dir
            if 'last-message.txt' in file_name:
                f = open(path_to_hg + '\\' + file_name, 'r')
                last_msg = f.readline()
                f.close()
                break
    except:    
        print('Error: Rep not found: ' + path_to_hg)
        raise SystemExit(0)                

    # If not found last commit msg
    if not last_msg:
        print('Error: last-message.txt in ' + path_to_hg + '[NOT FIND]')
        raise SystemExit(0)
    
    print('Info: Find last message: ' + last_msg)
    last_msg = last_msg[:last_msg.find(' ')]
    print('Info: Commit number: ' + last_msg)
    create_fw_ver_h(last_msg + param)
    
def main():
    param = ''
    type = 'mercurial'
    # Get param
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hp:g')
    except getopt.GetoptError as err:
        usage() # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        raise SystemExit(2)
    for o, a in opts:
        if o in ('-h'):
            usage()
            return
        elif o in ("-p"):
            param = a
            print('Info: Additional param: ' + param)
        elif o in ("-g"):
            type = 'git'
        else:
            return print("Undefined param" + o)
    print('Info: Type: ' + type)
    if type == 'mercurial':
        set_fw_ver_mercurial(param)
    elif type == 'git':
        raise SystemExit(0)

if __name__ == '__main__':
    main()