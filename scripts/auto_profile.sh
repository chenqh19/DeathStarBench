#!/bin/bash

# Check if both the output file name, number of loops, and sleep time are provided as parameters
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <profile_name> <num_loops> <loop_duration>"
    exit 1
fi

# Get the IDs of all running Docker containers
container_ids=$(sudo docker ps -q)

'''
Specify multiple keywords
'''
keywords=("UserTimeline" "PostStorage")
# keywords=("Service")

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

# Get the output file name, number of loops, and loop duration from parameters
profile_name="perf_files/$1"
num_loops="$2"
loop_duration="$3"
profile_time=$[loop_duration*5]

# Initialize the loop counter
count=0
# echo "count,gc,alloc,network,sched,lock" >> "$profile_name.txt"

# Main loop, execute for the specified number of loops
while [ $count -lt $num_loops ]; do
    # Execute the additional custom command before each loop and wait for it to finish

    # ./profile.sh "$profile_name-$count-" "sudo perf record  -F 99 -g --call-graph fp -p" "-- sleep $profile_time" "$all_pids" & wait
    # ./profile.sh "$profile_name-$count-" "sudo perf record  -F 99 -g --call-graph fp" "-- sleep $profile_time" "-a" & wait
    
    sudo perf stat -e cycles,instructions,cache-references,cache-misses,LLC-misses -a -- sleep $profile_time & wait

    # # Execute the custom command and store the output in the variable cmd_output
    # cmd_output_gc=$(./calculate.sh "$profile_name-$count-1".txt % gc scan sweep mark find grey gcDrain heapBitsSetType)
    # cmd_output_alloc=$(./calculate.sh "$profile_name-$count-1".txt % alloc)
    # cmd_output_network=$(./calculate.sh "$profile_name-$count-1".txt % tcp net xmit sock ip nf_ recv fib_ conn cond transport br_ smp_ __dev_forward_skb thrift grpc)
    # cmd_output_sched=$(./calculate.sh "$profile_name-$count-1".txt % steal sched psi_task_change interrupt_entry)
    # cmd_output_lock=$(./calculate.sh "$profile_name-$count-1".txt % lock utex)

    # # Append the loop counter and command output in comma-separated form to the output file
    # echo "$count,$cmd_output_gc,$cmd_output_alloc,$cmd_output_network,$cmd_output_sched,$cmd_output_lock" >> "$profile_name.txt"
    # Increment the loop counter
    count=$((count + 1))

    # Wait for the specified loop duration
    wait
    sleep "$loop_duration"
done
