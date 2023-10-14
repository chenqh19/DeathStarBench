#!/bin/bash

if [ "$#" -ne 3 ]; then
  echo "Usage: $0 <filename> <service_string> <func_string>"
  exit 1
fi

filename="$1"
service_string="$2"
func_string="$3"

# Filter lines containing $service_string from the specified file
grep "$service_string" "$filename" > filtered.txt

# Filter lines containing $func_string from the filtered file
grep "$func_string" filtered.txt > filtered_func.txt

# # Calculate the sum of numbers before the percent sign at the beginning of each line
# total=0
# while read -r line; do
#     # Extract the number before the percent sign at the beginning of each line
#     number=$(echo "$line" | grep -o '.*')
    
#     # Add the number to the total
#     total=$((total + number))
# done < filtered_func.txt

total=$(awk -F'%' '{ total += $1 } END { print total }' filtered_func.txt)

# Print the total
echo "Total: $total"

Clean up temporary files
rm filtered.txt filtered_func.txt
