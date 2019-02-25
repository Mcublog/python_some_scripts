import matplotlib.pyplot as plt
import math, os, numpy
import xml.etree.ElementTree as ET
from scipy.interpolate import spline


tree = ET.parse('test.xml')
root = tree.getroot()

plt.title("Temperature graphic", fontsize = 14)
plt.xlabel("Time", fontsize = 8)
plt.ylabel("Temperature", fontsize = 12)

x_val = []
x_tick = []
y_val = []

for report in root:
    timestamp = report.find('timestamp')
    time = timestamp.find('time').text
    x_val.append(int(report.get('id')))
    x_tick.append(time)
    hdc = report.find('hdc1080')
    temp = hdc.find('t').text
    temp = temp.replace(',', '.')
    y_val.append(float(temp))

plt.xticks(x_val, x_tick, rotation = 90)
print(x_val)
plt.grid()
plt.plot(x_val, y_val)
y_mean = numpy.mean(y_val)
ax = plt.gca()
ax.axhline(y=y_mean - 5, color='k')
ax.axvline(x=0, color='k')

mng = plt.get_current_fig_manager()
mng.window.state('zoomed')

plt.show()
