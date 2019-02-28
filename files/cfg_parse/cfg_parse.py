import os, sys, shutil


verbose = 0


def clear(version):
    if os.path.isdir(version):
        shutil.rmtree(version)
    os.mkdir(version)


def form_carray(num, reg_list, comment):
    cfg = '    {'
    if verbose:
        print('===========CFG===========')
    # j list ["reg name", "reg value"]
    for (i, reg) in enumerate(reg_list):
        if verbose:
            print(str(i) + ': ' + reg[0] + ': ' + str(int(reg[1], 16)))
        cfg += ' ' + str(int(reg[1], 16)) + ','
        if (i == (len(reg_list) - 1)):
            cfg = cfg[:-1] + ' }, //' + comment +'\n'
    if verbose:
        print('===========CFG===========\n')
        print(cfg)
    return cfg


def main():
    out_file_name = 'hw_afe_cfg_list'
    out_dir = 'cfg_out'
    
    in_dir = 'cfg_in'

    # Clear output dir
    clear(out_dir)
    
    print('file list: ' + str(os.listdir(in_dir)))
    file_list = os.listdir(in_dir)
    cfg_len = str(len(file_list)) # cfg[x][]
    
    # Create .h
    f = open(out_dir + '//' + out_file_name + '.h', 'w')
    f.write('#ifndef AFE_CFG_LIST_H_\n')
    f.write('#define AFE_CFG_LIST_H_\n\n')
    f.write('#include <stdint.h>\n\n')
    f.write('#define AFE_CFG_NUM (' + cfg_len + ')\n')
    f.write('#define AFE_CFG_LEN (49)\n\n')
    
    # Create array
    f = open(out_dir + '//' + out_file_name + '.h', 'a')
    f.write('static const uint32_t cfg[AFE_CFG_NUM][AFE_CFG_LEN] = \n{\n')
    cfg = ''
    for (i, file) in enumerate(file_list):
        fi = open(in_dir + '//' + file, 'r')
        reg_list = []
        for line in fi:
            reg_list.append(line.split('\t'))
        cfg += form_carray(i, reg_list, file)
        fi.close()
    f.write(cfg)
    f.write('};\n\n')
    f.write('#endif /* AFE_CFG_LIST_H_ */\n') 
    f.close()

    print('Convert complete: ' + out_dir + '/' + out_file_name + '.h')

if __name__ == '__main__':
    main()
