#!/bin/bash

# Start time
start_time=$(date +%s)

# Loop until 60 seconds have passed
while (( $(date +%s) - start_time < 60 )); do
  /usr/bin/python3 /home/pi/Onion/PythonScripts/version5.py
done
