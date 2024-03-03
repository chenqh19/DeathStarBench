def read_file(file_path):
    """Read file and return the content of each line"""
    with open(file_path, 'r', errors='ignore') as file:
        lines = file.readlines()
    return lines

def write_file(file_path, lines):
    """Write content to file"""
    with open(file_path, 'w') as file:
        file.writelines(lines)

def get_percentile(lat_list, percent):
    index = int(len(lat_list)*percent/100)
    return lat_list[index]

def get_distribution(lat_list):
    percents = [50, 90, 99]
    for p in percents:
        print(p, "% tail latency", get_percentile(lat_list, p))


def process_rpcs(file_a_path, file_b_path):
    """Process two files"""
    # Read the content of both files
    lines_a = read_file(file_a_path)
    lines_b = read_file(file_b_path)
    lats = []
    # Iterate over each line in file a
    for i, line_a in enumerate(lines_a):
        if i >= len(lines_b):
            break
        # Parse the content of each line
        parts_a = line_a.strip().split(',')
        if len(parts_a) < 3:
            lines_a.pop(i)
            continue
        j = 0
        while j < len(lines_b):
            line_b = lines_b[j]
            parts_b = line_b.strip().split(',')
            # Check if the second item matches
            if len(parts_b) < 3:
                lines_b.pop(j)
                continue
            if parts_a[1] == parts_b[1]:
                # If it matches, subtract the third item of file b from the third item of file a
                rpc_lat = int(parts_b[2]) - int(parts_a[2])
                lats.append(rpc_lat)
                lines_b.pop(j)  # Remove the matched line
                break
            else:
                j += 1  # Move to the next line
    # print(lats)
    lats.sort()
    return lats

def process_tcps(file_a_path, file_b_path):
    """Process two files"""
    # Read the content of both files
    lines_a = read_file(file_a_path)
    lines_b = read_file(file_b_path)
    lats = []
    # Iterate over each line in file a
    for i, line_a in enumerate(lines_a):
        # Iterate over each line in file b
        for j, line_b in enumerate(lines_b):
            # Compare if the current lines are the same
            if line_a[20:50] == line_b[20:50]:
                # Find the previous line in file a and file b where the current line in found
                a_prev_line = lines_a[i-1]
                b_prev_line = lines_b[j-1]
                # Parse the content of each line
                a_parts = a_prev_line.strip().split(',')
                b_parts = b_prev_line.strip().split(',')
                # Find the first number before the comma and calculate the difference
                
                a_num = safe_int_conversion(a_parts[0])
                b_num = safe_int_conversion(b_parts[0])
                if b_num is not None and a_num is not None:
                    diff = b_num - a_num
                    lats.append(diff)
                lines_b.pop(j)
                lines_b.pop(j-1)
                break
    lats.sort()
    return lats

def process_rpc_tcp(file_rpc_path, file_tcp_path):
    """Process two files"""
    # Read the content of both files
    lines_a = read_file(file_tcp_path)
    lines_b = read_file(file_rpc_path)
    lats = []
    # Iterate over each line in file a
    for i, line_a in enumerate(lines_a):
        # Parse the content of each line
        j = 0
        # print(line_a[5:50])
        while j < len(lines_b):
            line_b = lines_b[j]
            parts_b = line_b.strip().split(',')
            # Check if the second item matches
            # if i == 1:
            #     print(parts_b[1][4:49])
            if line_a[20:50] == parts_b[1][19:49]:
                # If it matches
                a_prev_line = lines_a[i-1]
                a_parts = a_prev_line.strip().split(',')
                a_num = safe_int_conversion(a_parts[0])
                if a_num is not None:
                    rpc_lat = abs(int(parts_b[2]) - a_num)
                lats.append(rpc_lat)
                lines_b.pop(j)  # Remove the matched line
            else:
                j += 1  # Move to the next line
    # print(lats)
    lats.sort()
    return lats

def safe_int_conversion(value):
    try:
        return int(value)
    except ValueError:
        return None

def remove_consecutive_times(filename):
    with open(filename, 'r+', errors='ignore') as file:
        lines = file.readlines()
        file.seek(0)
        prev_line_contains_time = False
        for line in lines:
            if "time" in line:
                if not prev_line_contains_time:
                    file.write(line)
                    prev_line_contains_time = True
            else:
                file.write(line)
                prev_line_contains_time = False
        file.truncate()

def remove_lines_with_time(filename, num_to_remove):
    lines = read_file(filename)

    filtered_lines = []
    skip = 0
    for line in lines:
        if "time" in line:
            skip = num_to_remove
        elif skip == 0:
            filtered_lines.append(line)
        else:
            skip -= 1

    with open(filename, 'w') as file:
        file.writelines(filtered_lines)

# filter problematic lines
remove_consecutive_times("ReadPostsA.txt")
remove_consecutive_times("ReadPostsB.txt")
remove_consecutive_times("ReadPostsC.txt")
remove_consecutive_times("ReadPostsD.txt")

remove_lines_with_time("ReadPostsA.txt", 1)
remove_lines_with_time("ReadPostsB.txt", 1)
remove_lines_with_time("ReadPostsC.txt", 1)
remove_lines_with_time("ReadPostsD.txt", 1)

remove_consecutive_times("htl-write_log.txt")
remove_consecutive_times("ps-read_log.txt")

remove_lines_with_time("htl-write_log.txt", 2)
remove_lines_with_time("ps-read_log.txt", 2)

# Process rpc files
rpc_result = process_rpcs("ReadPostsA.txt", "ReadPostsC.txt")
get_distribution(rpc_result)


rpc_result = process_rpcs("ReadPostsC.txt", "ReadPostsD.txt")
get_distribution(rpc_result)


rpc_result = process_rpcs("ReadPostsD.txt", "ReadPostsB.txt")
get_distribution(rpc_result)


'''
# # Process tcp files
tcp_result = process_tcps("htl-write_log.txt", "ps-read_log.txt")
percent = get_percentile(tcp_result, 99)
# print(tcp_result)
print("tail latency:", percent)

# Process one rpc file and one tcp file
# rt_result = process_rpc_tcp("ReadPostsA.txt", "htl-write_log.txt")
# print(len(rt_result))
'''