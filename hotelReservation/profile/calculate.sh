#!/bin/bash

if [ "$#" -lt 3 ]; then
  echo "Usage: $0 <filename> <service_string> <func_string1> [func_string2] [func_string3] ..."
  exit 1
fi

filename="$1"
service_string="$2"
shift 2  # Remove the first two arguments (filename and service_string)

# Combine all func_string arguments into a single regular expression
func_strings_regex=$(printf "|%s" "$@")
func_strings_regex=${func_strings_regex:1}  # Remove the leading '|'

# Filter lines containing $service_string and any of the func_strings
grep -i -E "$service_string.*($func_strings_regex)" "$filename" > filtered_func.txt

total=$(awk -F'%' '{ total += $1 } END { print total }' filtered_func.txt)

# Print the total
echo "Total: $total"

# Clean up temporary files
rm filtered_func.txt
