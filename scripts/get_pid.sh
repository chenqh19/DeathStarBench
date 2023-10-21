#!/bin/bash

# Get the IDs of all running Docker containers
container_ids=$(sudo docker ps -q)

# Specify multiple keywords
keywords=("Text")

# Initialize a variable to store all PIDs
all_pids=""

# Loop through each container ID and run sudo docker top
for container_id in $container_ids; do
    echo "Running sudo docker top for container $container_id"
    top_result=$(sudo docker top $container_id)
    
    found=false
    
    # Use awk and grep to extract lines containing keywords and get PIDs
    for keyword in "${keywords[@]}"; do
        pid_list=$(echo "$top_result" | awk -v keyword="$keyword" '$8 ~ keyword {print $2}')
        if [ -n "$pid_list" ]; then
            found=true
            if [ -n "$all_pids" ]; then
                all_pids="${all_pids},${pid_list}"
            else
                all_pids="${pid_list}"
            fi
            break
        fi
    done
    
    if [ "$found" = true ]; then
        echo "Container $container_id contains processes with one of the keywords: ${keywords[*]}"
    fi
done

# Output all extracted PIDs, separated by commas
echo "All PIDs with one of the keywords: ${keywords[*]}: $all_pids"
