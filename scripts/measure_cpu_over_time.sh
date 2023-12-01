#!/bin/bash

# Parse command-line arguments
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <monitoring_duration_seconds>"
    exit 1
fi

# Set the monitoring duration based on the provided argument
monitoring_duration=$1

# Initialize start time
start_time=$(date +%s)

# Initialize sum and count variables
sum=0
count=0

# Run the loop until the specified duration is reached
while [ $(( $(date +%s) - $start_time )) -lt $monitoring_duration ]; do
    # Run top in batch mode for one sample, extract CPU usage, and add to sum
    sample_value=$(top -b -n 1 | grep "Cpu(s)" | awk '{print $2+$4}')
    sum=$(awk "BEGIN {print $sum + $sample_value}")
    count=$((count + 1))
    
    # Optional: Add a delay between samples (adjust as needed)
    sleep 3
done

# Calculate the average
average=$(awk "BEGIN {print $sum / $count}")

echo "Average CPU Utilization: $average%"

