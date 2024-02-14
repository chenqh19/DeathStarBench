import numpy as np
import matplotlib.pyplot as plt

def find_second_smallest(numbers):
    unique_numbers = sorted(set(numbers))
    if len(unique_numbers) > 1:
        return unique_numbers[1]
    else:
        return None

def main():
    count = 0
    results = []
    with open('../kuber-deploy/test_rps-searchaway.txt', 'r') as file:
        lines = file.readlines()
        for i in range(len(lines)):
            if "new_config" in lines[i]:
                if i + 5 < len(lines):
                    numbers = [float(line.split()[0]) for line in lines[i+1:i+6]]
                    second_smallest = find_second_smallest(numbers)
                    if second_smallest is not None:
                        results.append(second_smallest)
                    else:
                        print(f"Not enough numbers at {count} to find the latency.")
                count += 1
    print(results)
    # final_array = np.zeros((17, 17))
    # c = 0
    # # no_part_result = results[0]
    # # c = 1
    # row_len = 17 # a bug: the third partition will never be 1
    # while row_len > 0:
    #     print(row_len, c)
    #     for i in range(c, c+row_len):
    #         final_array[17-row_len][i-c] = results[i]
    #     c = c+row_len
    #     row_len -= 1
    # print(final_array)
    # plt.imshow(final_array, cmap='viridis', interpolation='nearest', vmin=20, vmax=200)
    # plt.colorbar()
    # plt.savefig('heatmap.png')




    

    print(f"Total count: {count}")

if __name__ == "__main__":
    main()
