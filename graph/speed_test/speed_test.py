import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import os, sys

import speed_test_parse as stp

# block_number = 'test_data'
block_number = '4096'
# block_number = '2048'
# block_number = '1024'
# block_number = '512'

f = open(os.getcwd() + '\\test\\' + block_number +'.txt', 'r')
data = f.read()
f.close()

numbers = stp.get_param(data, 'block num')
speeds = stp.get_param(data, 'speed')

#print(speeds)
#print(numbers)

# Create plots
fig, ax = plt.subplots()
plt.xlabel("Block number", fontsize = 12)
# Generate a list from 0 to report number
plt.title('LittleFS write speed test (4MB filesize)', fontsize = 14)
plt.ylabel('Bytes\s', fontsize = 12)

ydata = []
xdata = []

for speed, num in zip(speeds, numbers):
    ydata.append(float(speed))
    xdata.append(int(num))
    
ax.plot(xdata, ydata, 'b-', label= block_number + ' byte block')

# Create x_tick, grid and legend
plt.xticks(xdata, rotation = 90)
ax.xaxis.set_major_locator(plt.MaxNLocator(50))
plt.grid(linestyle = 'dashed')
legend = ax.legend(loc='best')

# Set the origin
ax.axhline(y = 0, color = 'k')
ax.axvline(x = 0, color = 'k')

# Set fig to fullscreen
mng = plt.get_current_fig_manager()
mng.window.state('zoomed')

plt.show()




