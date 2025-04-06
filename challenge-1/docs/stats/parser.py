import re
import csv

# Input log file and output CSV file
log_file = "log.txt"  # Change this to your actual log file name
csv_file = "state_durations.csv"

# Regular expression to match the key-value pairs
pattern = re.compile(r"(Idle|Measurement|Wifi on|TX):\s*(\d+)")

# Read the log file and extract data
entries = []
with open(log_file, "r") as file:
    entry = {}
    for line in file:
        match = pattern.search(line)
        if match:
            key, value = match.groups()
            entry[key] = int(value)
        elif "ets Jul" in line and entry:  # New log entry found, save the previous
            entries.append(entry)
            entry = {}  # Reset for next entry
    if entry:  # Append the last entry if present
        entries.append(entry)

# Write to CSV (append mode)
headers = ["Idle", "Measurement", "Wifi on", "TX"]
file_exists = False
try:
    with open(csv_file, "r") as f:
        file_exists = True
except FileNotFoundError:
    pass

with open(csv_file, "a", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    if not file_exists:
        writer.writeheader()  # Write headers only if the file is new
    writer.writerows(entries)  # Append new rows

print(f"Parsed {len(entries)} log entries and appended to {csv_file}.")
