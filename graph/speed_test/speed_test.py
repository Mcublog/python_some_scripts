import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import os, sys

import speed_test_parse as stp

# block_size = 'test_data'
# block_size = '4096'
# block_size = '2048'
# block_size = '1024'
# block_size = '512'
# block_size = '256'
# block_size = '120'

# block_size = '4096r'
# block_size = '2048r'
# block_size = '1024r'
# block_size = '512r'
block_size = '256r'
# block_size = '120r'


f = open(os.getcwd() + '\\test\\' + block_size +'.txt', 'r')
data = f.read()
f.close()

read = True if 'r' in block_size else False
if read:
    block_size = block_size[:-1]

time_start = stp.get_param(data, 'start time')
time_stop = stp.get_param(data, 'stop time')

if block_size.isdigit() == False:
    block_size = '16536'

print(block_size)
speeds = []
for start, stop in zip(time_start, time_stop):
    difftime = int(stop) - int(start)
    if difftime <= 0:
        difftime = 1
    speeds.append(float(block_size) * 1000 / float(difftime))

# Create plots
fig, ax = plt.subplots()
fig.canvas.set_window_title(block_size)
plt.xlabel("Block number", fontsize = 12)

# Generate a list from 0 to speeds len
xdata = range(len(speeds))
plt.title('LittleFS write speed test (4MB filesize)', fontsize = 14)
plt.ylabel('Bytes\\s', fontsize = 12)
  
ax.plot(xdata, speeds, 'b-', label = block_size + ' byte block')

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
