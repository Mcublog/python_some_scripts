import os, shutil

# Find last commit msg
path_to_hg = os.getcwd()[:-len('MDK-ARM')] + '.hg'
print('Info: Go to --> ' + path_to_hg)
last_msg = ''
for file_name in os.listdir(path_to_hg):  # for each file in dir
    if 'last-message.txt' in file_name:
        f = open(path_to_hg + '\\' + file_name, 'r')
        last_msg = f.readline()
        f.close()
        break

# If not found last commit msg
if not last_msg:
    print('Error: last-message.txt in ' + path_to_hg + '[NOT FIND]')
    raise SystemExit(0)
    
print('Info: Find last message: ' + last_msg)
last_msg = last_msg[:last_msg.find(' ')]
print('Info: Commit number: ' + last_msg)

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

exit()