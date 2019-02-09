import matplotlib.pyplot as plt
import math


plt.title("Test graph", fontsize = 24)
plt.xlabel("Value", fontsize = 14)
plt.ylabel("Func of value", fontsize = 14)
x_val = list(range(1, 100))
y_val = [math.lgamma(x) for x in x_val]
plt.plot(x_val, y_val)
plt.show()