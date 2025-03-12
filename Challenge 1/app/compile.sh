#!/bin/bash

# Activate PlatformIO virtual environment
source /home/iotpolimi/.platformio/penv/bin/activate

# Change to the specified directory
cd /home/matteo/Coding/projects-iot-2025/Challenge\ 1/app || exit

# Run PlatformIO build
pio run