import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
from scipy.interpolate import spline
import math, os, numpy


# Set path to data file
current_path = os.path.dirname(os.path.realpath(__file__))
data_path = current_path + '\\data'
dir_list = os.listdir(data_path)
file_list = os.listdir(data_path + '\\' + dir_list[0])

file_list.sort()
idx = 0
for (i, file) in enumerate(file_list):
    if ('tph_report' in file):
        print ('file: ' + file)
        idx = i
        break;
print(idx)
del file_list[0:idx]
print(file_list)

print('Tph report files in dir: ' + str(len(file_list)))

tree = ET.parse(data_path + '\\' + dir_list[0] + '\\' + file_list[0])
root = tree.getroot()

x_val = [] # x value like 1, 2, 3 and etc
x_tick = [] # x ticks like 10:42:30:513, 10:42:31:513 and etc
hdc_temp = [] # temperature from hdc1080  
lps_temp = [] # temperature from lps331

for report in root:
    # Get node timestamp for x_ticks
    timestamp = report.find('timestamp')
    time = timestamp.find('time').text
    x_val.append(int(report.get('id')))
    x_tick.append(time) # Append time for current id
    
    # Get temp from hdc1080 node
    hdc = report.find('hdc1080')
    temp = hdc.find('t').text
    temp = temp.replace(',', '.')
    hdc_temp.append(float(temp))
    
    # Get temp from lps331 node
    hdc = report.find('lps331')
    temp = hdc.find('t').text
    temp = temp.replace(',', '.')
    lps_temp.append(float(temp))


# Create plots
fig, ax = plt.subplots()
plt.title("Temperature graphic", fontsize = 14)
plt.xlabel("Time", fontsize = 8)
plt.ylabel("Temperature", fontsize = 12)
ax.plot(x_val, hdc_temp, 'r-', label='hdc_temp')
ax.plot(x_val, lps_temp, 'y-', label='lps331')

# Create x_tick, grid and legend
plt.xticks(x_val, x_tick, rotation = 90)
plt.grid(linestyle = 'dashed')
legend = ax.legend(loc='best')

# Set the origin
y_mean = numpy.mean(hdc_temp)
ax.axhline(y = y_mean - y_mean/10, color = 'k')
ax.axvline(x = 0, color = 'k')

# Set fig to fullscreen
mng = plt.get_current_fig_manager()
mng.window.state('zoomed')

plt.show()