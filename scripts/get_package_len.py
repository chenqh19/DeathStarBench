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

filename = 'logs.txt'  
result = find_numbers_after_commas(filename)
print("Numbers found after ',,,,,':", result)
