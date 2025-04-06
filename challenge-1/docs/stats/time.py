import numpy as np
import matplotlib.pyplot as plt

def formula(x):
    # compute the energy consumption of each cycle
    # 0.213 is the energy consumption of transmission, wifi on, sensor reading and idle
    energy_consumption = (0.05966 * X) + 0.213
    # compute the number of cycles before the battery is fully drained
    number_of_cycles = 17886 / energy_consumption
    # compute an approximation of the lifetime of the battery in seconds
    battery_lifetime_seconds = number_of_cycles * x
    # compute and return the lifetime of the battery in hours
    battery_lifetime_hours = battery_lifetime_seconds / 3600
    return battery_lifetime_hours

X = np.linspace(1, 1000, 1000)
Y = formula(X)

# Plot the function
plt.figure(figsize=(8, 5))
plt.plot(X, Y, color='b')
plt.xlabel('Deep Sleep Time (seconds)')
plt.ylabel('Battery Duration (hours)')
plt.title('Deep Sleep vs Battery Duration')
plt.grid()
plt.show()
