import re
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# -*- coding: utf-8 -*-
import urllib.request  # url request
import time

def find_strings_after_a(file_path, target_string, container_set):
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # get container id
            matches = re.findall(f'{re.escape(target_string)}(.{{16}})', line)
            for match in matches:
                match = "http://localhost:16686/api/traces/" + match + "?prettyPrint=true"
                if match not in container_set:
                    container_set.append(match)
                    print(f"found: {match}")


container_set = []
file_path = 'traces.txt'
target_string = "traceID\":\""

find_strings_after_a(file_path, target_string, container_set)

print(container_set)


def download_file(url, save_path):
    response = requests.get(url)

    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"Download successfully to: {save_path}")
    else:
        print(f"Downloda failed with code: {response.status_code}")


file_path = 'traces_files/'
cnt = 0
for container_path in container_set:
    download_file(container_path, file_path+str(cnt)+".txt")
    cnt += 1




def extract_number_from_line(line, pattern):
    # match = re.search(pattern, line)
    # if match:
    #     return int(match.group())
    # return None
    numbers = re.findall(r'\d+', line)
    numbers = [int(num) for num in numbers]
    return numbers[0]

def process_file(file_path, pattern_a, pattern_b, pattern_c, pattern_d):
    result_b = -1
    result_d = -1

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        number_b = None
        number_d = None
        for i, line in enumerate(lines):
            if pattern_a in line:
                # check whether the row contains a
                index_b = i + 1
                while index_b < len(lines) and pattern_b not in lines[index_b]:
                    index_b += 1

                if index_b < len(lines):
                    # find the number in next b
                    number_b = extract_number_from_line(lines[index_b], pattern_b)
            if pattern_c in line:
                # check whether the row contains c

                index_d = i + 1
                while index_d < len(lines) and pattern_d not in lines[index_d]:
                    index_d += 1

                if index_d < len(lines):
                    # find the number in next d
                    number_d = extract_number_from_line(lines[index_d], pattern_d)

    # get duration
    if number_b is None:
        return None
    if number_d is None:
        return None
    result = number_b - number_d

    return result, number_d

# examples
pattern_a = 'check_overhead_client'  
pattern_b = 'duration'  
pattern_c = 'post_storage_read_posts_server'  
pattern_d = 'duration'  

results = []
pure_execution_times = []
for i in range(len(container_set)):
    result, d = process_file(file_path+str(i)+".txt", pattern_a, pattern_b, pattern_c, pattern_d)
    results.append(result)
    pure_execution_times.append(d)

print("ovrehead:", results)

def calculate_statistics(data):
    # Filter out "None" values from the data
    filtered_data = [value for value in data if value is not None]

    if not filtered_data:
        print("No valid data in the array.")
        return None, None, None, None, None, None

    # Calculate mean
    mean_value = sum(filtered_data) / len(filtered_data)

    # Calculate minimum and maximum
    min_value = min(filtered_data)
    max_value = max(filtered_data)

    # Calculate quartiles
    sorted_data = sorted(filtered_data)
    n = len(sorted_data)
    q1_index = (n - 1) // 4
    q2_index = (n - 1) // 2
    q3_index = 3 * (n - 1) // 4

    q1 = sorted_data[q1_index]
    q2 = sorted_data[q2_index]
    q3 = sorted_data[q3_index]

    return mean_value, min_value, q1, q2, q3, max_value

# Example usage
data_array = [1, 2, 3, None, 4, 5, 6, None, 7, 8, 9]
mean, minimum, q1, median, q3, maximum = calculate_statistics(results)
mean_func, _1, _2, _3, _4, _5 = calculate_statistics(pure_execution_times)

if mean is not None and minimum is not None and q1 is not None and median is not None and q3 is not None and maximum is not None:
    print(f"Mean_function time: {mean_func}")
    print(f"Mean: {mean}")
    print(f"Minimum: {minimum}")
    print(f"Lower Quartile (Q1): {q1}")
    print(f"Median (Q2): {median}")
    print(f"Upper Quartile (Q3): {q3}")
    print(f"Maximum: {maximum}")


def delete_files_in_folder(folder_path):
    try:
        # List all files in the folder
        files = os.listdir(folder_path)

        # Iterate through files and delete each one
        for file_name in files:
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print(f"All files in the folder have been deleted.")
    except Exception as e:
        print(f"Failed to delete files in the folder: {e}")

delete_files_in_folder(file_path)