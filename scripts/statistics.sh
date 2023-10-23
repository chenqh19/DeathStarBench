#!/bin/bash

# Check the number of command-line arguments
if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <folder_path> <command1> <command2> <output_file>"
    exit 1
fi

# Get folder path, command, and output file name from command-line arguments
folder_path="$1"
command1="$2"
command2="$3"
output_file="$4"

echo -n "$folder_path," >> $output_file
# Use 'ls' to list files in the folder, sort them by file name, and iterate through them
for file in $(ls -1tr "$folder_path"); do
    full_path="$folder_path/$file"
    if [ -f "$full_path" ]; then
        # Execute the command and append the result to the output file, separated by a comma
        result=$($command1 "$full_path" $command2)
        echo -n "$result," >> $output_file
    fi
done

echo >> $output_file

