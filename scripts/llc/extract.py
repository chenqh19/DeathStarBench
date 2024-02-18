import numpy as np
import matplotlib.pyplot as plt

def find_second_smallest(numbers):
    unique_numbers = sorted(set(numbers))
    if len(unique_numbers) > 1:
        return unique_numbers[1]
    else:
        return None

def find_mid_avg(numbers):
    unique_numbers = sorted(set(numbers))
    if len(unique_numbers) > 1:
        return round((unique_numbers[1]+unique_numbers[2]+unique_numbers[3])/3, 1)
    else:
        return None

def main():
    count = 0
    results = []
    with open('../lat_files/ps_rps-local.txt', 'r') as file:
        lines = file.readlines()
        for i in range(len(lines)):
            if "new_config" in lines[i]:
                if i + 5 < len(lines):
                    numbers = [float(line.split()[0]) for line in lines[i+1:i+6]]
                    rep_num = find_mid_avg(numbers)
                    if rep_num is not None:
                        results.append(rep_num)
                    else:
                        print(f"Not enough numbers at {count} to find the latency.")
                count += 1
    print(results)
    # arr_size = 6
    # final_array = np.zeros((arr_size, arr_size))
    # c = 0
    # # no_part_result = results[0]
    # # c = 1
    # row_len = arr_size 
    # while row_len > 0:
    #     print(row_len, c)
    #     for i in range(c, c+row_len):
    #         final_array[i-c][row_len-1-(i-c)] = results[i]
    #     c = c+row_len
    #     row_len -= 1
    # print(final_array)
    # plt.imshow(final_array, cmap='viridis', interpolation='nearest', vmin=15, vmax=50)
    # plt.colorbar()
    # plt.savefig('heatmap.png')




    

    print(f"Total count: {count}")

if __name__ == "__main__":
    main()
