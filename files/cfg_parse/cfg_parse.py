import os, sys, shutil
import getopt


verbose = 0


def clear(version):
    if os.path.isdir(version):
        shutil.rmtree(version)
    os.mkdir(version)


def form_carray(num, reg_list, comment):
    cfg = 'uint32_t cfg' + str(num) + '[] = ['
    if verbose:
        print('===========CFG===========')
    # j list ["reg name", "reg value"]
    for (i, reg) in enumerate(reg_list):
        if verbose:
            print(str(i) + ': ' + reg[0] + ': ' + str(int(reg[1], 16)))
        cfg += ' ' + str(int(reg[1], 16)) + ','
        if (i == (len(reg_list) - 1)):
            cfg = cfg[:-1] + ' ] //' + comment +'\n'
    if verbose:
        print('===========CFG===========\n')
        print(cfg)
    return cfg


def main():
    out_file_name = 'afe_cfg_list.c'
    out_dir = 'cfg_out'
    
    in_dir = 'cfg_in'
    
    # Clear output dir
    clear(out_dir)
    
    print('file list: ' + str(os.listdir(in_dir)))
    file_list = os.listdir(in_dir)
    
    for (i, file) in enumerate(file_list):
        f = open(in_dir + '//' + file, 'r')
        reg_list = []
        for line in f:
            reg_list.append(line.split('\t'))
    
        cfg = form_carray(i, reg_list, file)
        f.close()
    
        # Open output file
        f = open(out_dir + '//' + out_file_name, 'a')
        f.write(cfg)
        f.close()
    print('Convert complete: ' + out_dir + '/' + out_file_name)

if __name__ == '__main__':
    main()
