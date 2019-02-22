import os, sys, shutil


sep_type = '//----------------------------------------------------------------------------\n'


def naming_sep(name, indent = 25):
    sep_indent = sep_type[indent:]
    sep_naming = sep_type[0:indent]
    for i in range(len(name)):
        sep_indent=sep_indent.replace(sep_indent[i], name[i], 1)
    sep_naming = sep_naming + sep_indent
    return sep_naming
    
    
def add_section(file, name = '', str_indent = 25, tab = 0, text = '', s = 1):
    """
    brief: adds a section of the following format:
    
    (tab)-----------(name)------------ <= if (s) == 1
    (str_indent)---^
    (text) bla bla...
    (tab)----------------------------- <= if (s) == 1
    
    param: file for writing
    param: name of section
    param: indent name in separator
    param: number of tabulation
    param: inner text in section
    param: up and down separators on/off, by default on
    return:
    """
    indent = '' # Indent start of string
    for i in range(tab):
        indent += '    '
    
    # Form start separator
    if not name == '':
        file.write(indent + naming_sep(name, str_indent))
    else:
        if s:# Add start separator
            file.write(indent +sep_type + '\n')
    
    # Form inner text
    if not text == '':
        if not text.count('\n'):
            file.write(indent + text + '\n')
        else:
            text_list = text.split('\n')
            for line in text_list:
                file.write(indent + line + '\n')

    if s:# Add end separator
        file.write(indent + sep_type + '\n')


def add_task_example(file, name, text):
    file.write('\n')
    add_section(file, name, text = text)


def add_function_definition(file, name = '', func_text = ''):
    file.write('\n')
    add_section(file, text = func_text, s = 0)


def main():
    out_file_name = 'main.c'
    
    func_declaration = 'uint32_t _func_proto(uint32_t param);'
    
    task_example = 'void ExampleTask (void *pvParameters);'
    sem_example = '//xSemaphoreHandle xbExmpl;'
    queue_example = '//xQueueHandle xqMsg;'
    
    sem_create = '//SemaphoreCreateBinary(xbExmpl);'
    queue_create = '//xqMsg = xQueueCreate(8, sizeof(msg_t));'
    task_create = (
                    'xTaskCreate(ExampleTask, "ExampleTask", '
                    'configMINIMAL_STACK_SIZE, NULL, tskIDLE_PRIORITY, NULL);'
                   )
    
    sem_take = '//xSemaphoreTake(xbExmpl, portMAX_DELAY);'
    
    task_text = (
                    'void ExampleTask (void *pvParameters)\n'
                    '{\n'
                    '   while(1)\n'
                    '   {\n'
                    '       vTaskDelay(1000);\n'
                    '   }\n'
                    '}'
                )
    
    func_proto = (
                    '/*-----------------------------------------------------------\n'
                    '/brief:\n'
                    '/param:\n'
                    '/return:\n'
                    '-----------------------------------------------------------*/\n'
                    'uint32_t _func_proto(uint32_t param)\n'
                    '{\n'
                    '   return 0;\n'
                    '}'
                 )


    # Create out_file_name
    print('Create: ' + out_file_name)
    f = open(out_file_name, 'w')
    
    f.write('#include "main.h"\n')
    f.write('#include "cmsis_os.h"\n\n')
    
    add_section(f, "Types and definition")
    add_section(f, "Local variables and fucntion", text = func_declaration)
    add_section(f, "Project options")
    add_section(f, "Task list",         text = task_example)
    add_section(f, "Semaphore list",    text = sem_example)
    add_section(f, "Queue list",        text = queue_example)

    f.write(naming_sep("Programm entry point")) # Start separator of main
    
    f.write('int main(void)\n')
    f.write('{\n')
    # Start inner section of main()
    add_section(f, "HW init", tab = 1)
    add_section(f, "Creating semaphores", tab = 1, text = sem_create)
    add_section(f, "Creating queues",     tab = 1, text = queue_create)
    add_section(f, "Creating tasks",      tab = 1, text = task_create)
    add_section(f, "Semaphores takes",    tab = 1, text = sem_take)
    
    f.write((
    '    osKernelStart();\n'
    '    while (1)\n'
    '    {\n'
    '    }\n'
    ))
    # End inner section of main()
    f.write('}\n')
    
    f.write(sep_type)# End separator main
    
    add_task_example(f, 'ExampleTask', text = task_text)
    add_function_definition(f, func_text = func_proto)
    f.close()
    print(out_file_name + ' is created')


if __name__ == '__main__':
    main()
