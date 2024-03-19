import os

def list_txt_files_in_current_directory():
    txt_files = [file for file in os.listdir() if file.endswith('.txt')]
    return txt_files

def find_numbers_after_commas(filename):
    numbers = []
    with open(filename, 'r') as file:
        for line in file:
            parts = line.split(',,,,,')
            for part in parts[1:]:  # Ignore the first part before the first ",,,,,"
                try:
                    number = int(part.strip().split()[0])
                    numbers.append(number)
                except (IndexError, ValueError):
                    # If there's no number or it's not a valid integer, ignore and continue
                    pass
    return numbers



filelist = ['search_logs.txt', 'rate_logs.txt', 'user_logs.txt', 'profile_logs.txt', 'reservation_logs.txt', 'recommendation_logs.txt', 'geo_logs.txt', 'frontend_logs.txt']
ave_len = []
for filename in filelist:
    arr = find_numbers_after_commas(filename)
    if len(arr) == 0:
        average = "None"
    else:
        average = round(sum(arr)/len(arr), 1)
    ave_len.append(average)

print(ave_len)
    
    


