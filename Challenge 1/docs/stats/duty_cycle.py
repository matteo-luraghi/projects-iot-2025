import numpy as np
import matplotlib.pyplot as plt

# Define states with (name, duration in seconds, power in milliwatts)
states = [
    ("idle1", 822e-6, 310.88),
    ("measurement", 29.34e-6, 466.74),
    ("idle2", 11.54e-3, 310.88),
    #("wifi on", 248e-3, 776.62),
    #("transmission", 728.1e-6, 221.76),
    ("idle3", 49.8e-3, 310.88),
    ("deep sleep", 41, 59.66),
]

# Generate time and power lists
time_points = [0]
power_values = []
labels = []
current_time = 0

for state, duration, power in states:
    power_values.append(power)
    current_time += duration
    time_points.append(current_time)
    labels.append(state)

# Plot the duty cycle
plt.figure(figsize=(10, 5))
plt.step(time_points[:-1], power_values, where='post', label="Power Consumption")
plt.xlabel("Time (s)")
plt.ylabel("Power (mW)")
plt.title("Sensor Duty Cycle Power Consumption")
plt.grid(True)

# Annotate states
for i, state in enumerate(labels):
    plt.text((time_points[i] + time_points[i + 1]) / 2, power_values[i] + 10, state,
             ha='center', va='bottom', fontsize=9, rotation=45)

plt.show()

