import os, sys, shutil

sep = '//----------------------------------------------------------------------------\n'

def naming_sep(name, indent = 25):
    sep_indent = sep[indent:]
    sep_naming = sep[0:indent]
    for i in range(len(name)):
        sep_indent=sep_indent.replace(sep_indent[i], name[i], 1)
    sep_naming = sep_naming + sep_indent
    return sep_naming
    
    
def add_section(file, name, str_indent = 25, tab = 0):
    indent = ''
    for i in range(tab):
        indent += '    '
    file.write(indent + naming_sep(name, str_indent))
    file.write(indent + sep + '\n')


def main():
    out_file_name = 'main.c'
    
    print('Separator len: ' + str(len(sep)))
    # Create .c
    print('Create: ' + out_file_name)
    f = open(out_file_name, 'w')
    
    f.write('#include "main.h"\n')
    f.write('#include "cmsis_os.h"\n\n')
    
    add_section(f, "Types and definition")
    add_section(f, "Project options")
    add_section(f, "Task list")
    add_section(f, "Semaphore list")
    add_section(f, "Queue list")

    f.write(naming_sep("Programm entry point"))
    
    f.write('int main(void)\n')
    f.write('{\n')
    # Start inner section
    add_section(f, "HW init", tab = 1)
    add_section(f, "Creating semaphores", tab = 1)
    add_section(f, "Creating tasks", tab = 1)
    add_section(f, "Semaphores init", tab = 1)
    add_section(f, "Queue list", tab = 1)
    # End inner section
    f.write('}\n')
    
    f.write(sep)
    
    f.close()
    print(out_file_name + ' is created')

if __name__ == '__main__':
    main()
