import csv
import os

def process_csv_and_txt(csv_filename, txt_filename, target_value):
    # # read csv
    # matching_values = []
    # with open(csv_filename, 'r', newline='', encoding='utf-8') as csv_file:
    #     csv_reader = csv.reader(csv_file)
    #     for row in csv_reader:
    #         if len(row) > 1 and row[1].strip() == target_value:
    #             matching_values.append(row[0].strip().lower())

    matching_values = ["mallocgc", "heapbitssettype", "nextfreefast", "memclrnoheappointers", "newobject", "allocspan", "nextfree", "refill"]


    # read txt & sum up
    total_percentage = 0
    each_percentage = {}

    with open(txt_filename, 'r', encoding='utf-8') as txt_file:
        for line in txt_file:
            line = line.strip().lower()
            for value in matching_values:
                if value in line:
                    # get matched
                    try:
                        percentage = float(line.split()[0].strip('%'))
                        each_percentage[value] = percentage
                        total_percentage += percentage
                        # print(value)
                    except ValueError:
                        print(f"Warning: Unable to extract percentage from line: {line}")

    # print sum
    print(f"File: {txt_filename}, Total Percentage: {format(total_percentage, '.2f')}%")
    print("Each percentage:", each_percentage)

# parameters
directory_path = './perf_files'
txt_filenames = 'origspan-GC1k'
csv_filename = 'names_hr.csv'
target_value = 'malloc'

def process_hr_files_in_directory(directory_path, target_files, csv_filename, target_value):
    # 获取目录下所有文件名含有"<txt_filenames>-"的txt文件
    hr_files = [filename for filename in os.listdir(directory_path) if filename.startswith(target_files) and filename.endswith(".txt")]

    # 逐个处理文件
    for hr_file in hr_files:
        file_path = os.path.join(directory_path, hr_file)
        process_csv_and_txt(csv_filename, file_path, target_value)

# execute
process_hr_files_in_directory(directory_path, txt_filenames, csv_filename, target_value)
