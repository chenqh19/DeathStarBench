import csv

def process_csv_and_txt(csv_filename, txt_filename, target_value):
    # read csv
    matching_values = []

    with open(csv_filename, 'r', newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if len(row) > 1 and row[1].strip() == target_value:
                matching_values.append(row[0].strip().lower())

    # read txt & sum up
    total_percentage = 0

    with open(txt_filename, 'r', encoding='utf-8') as txt_file:
        for line in txt_file:
            line = line.strip().lower()
            for value in matching_values:
                if value in line:
                    # get matched
                    try:
                        percentage = float(line.split()[0].strip('%'))
                        total_percentage += percentage
                        print(value)
                    except ValueError:
                        print(f"Warning: Unable to extract percentage from line: {line}")

    # print sum
    print(f"Total Percentage: {total_percentage}%")

# parameters
csv_filename = 'names_hr.csv'
txt_filename = 'hr-gc0-2724237-0-0.txt'
target_value = 'GC'

# execute
process_csv_and_txt(csv_filename, txt_filename, target_value)
