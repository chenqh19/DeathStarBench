#!/bin/bash

# Check if there are enough arguments
if [ $# -lt 4 ]; then
  echo "Usage: $0 <name> <first_half_command> <third_half_command> <second_half1> [<second_half2> ...]"
  exit 1
fi

# Extract the first half of the command
name="$1"
first_half="$2"
third_half="$3"
shift 3

# Iterate through the second half arguments, combine and execute commands one by one
i=1
for second_half in "$@"; do
  full_command="$first_half $second_half $third_half"
  echo "Executing command: $full_command"
  # Execute the command using eval
  eval "$full_command & wait"
  
  # Execute an additional command
  report_command="sudo perf report --no-children > perf_files/$name$i.txt"
  echo "Executing an additional command: $report_command"
  eval "$report_command & wait"

  i=$((i + 1))
  # If you want to wait for each command to finish before proceeding, you can change the previous line to: i=$((i + 1)) && eval "$report_command & wait"
done

echo "All commands executed"
