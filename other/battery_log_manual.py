import os, sys
import datetime

log_name = 'battery_log.txt'

print('Enter charge: ')
charge = input()
if not charge.isdigit():
    print('Uncorrect charge value: ' + charge)
    sys.exit(0)
    
percent = int(charge)
if percent > 100:
    print('Uncorrect charge value: ' + charge)
    sys.exit(0)
    
print('Current charge: ' + str(percent) +'%')
print('Added record to file: ' + log_name)

file_exist = 1;
try:
    f = open(log_name, 'r')
except:
    f = open(log_name, 'w') # Create file
    file_exist = 0

if file_exist:
    f = open(log_name, 'a')
    
f.write(str(datetime.datetime.now()) + ' Charge: ' + str(percent) + '%\r\n')
f.close()


