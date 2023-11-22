import matplotlib.pyplot as plt
import numpy as np

def plot_multiple_box_plots(data_sets, output_file, y_threshold):
    fig, ax = plt.subplots(figsize=(12, 6))
    over_vals = []
    for i, dataset in enumerate(data_sets):
        if dataset[-1] > y_threshold:
            over_vals.append(dataset[-1])
            data_sets[i][-1] = y_threshold
        else:
            over_vals.append(0)
            
    print(over_vals)
    bplot = ax.boxplot(data_sets, vert=True, widths=0.5, patch_artist=True)

    # ax.set_xticklabels([f'Data {i+1}' for i in range(len(data_sets))])
    # ax.set_xticklabels(["1-node\n10k posts", "1-node\n200k posts", "2-node\n10k posts", "2-node\n200k posts"])
    ax.set_xticklabels(["text", "user-mention", "creator", "media", "urls", "unique-id", 
                        "store-post", "write-utl", "social-graph", "write-htl"])
    ax.set_ylabel('Remote function call overhead (us)')

    # Customize box colors
    colors = ["lightcyan", 'lightsteelblue', 'lightskyblue', 'lightseagreen', 'lightgreen', 
                'lightyellow', 'lightpink', 'lightsalmon', 'lightgray', 'lightslategray']
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)

    # Set y-axis limit
    plt.ylim(0, y_threshold)

    # Annotate values at the top
    i = 0
    for max_value in over_vals:
        if max_value > y_threshold:
            ax.annotate(f'{max_value}', xy=(i + 1, y_threshold), xytext=(i + 1.1, y_threshold-30),
                        arrowprops=dict(facecolor='black', arrowstyle='->'))
        i += 1

    plt.title('Function call at 1-node, 10k posts')
    plt.savefig(output_file)
    plt.show()

# Example usage with multiple data sets
# data_set1 = [96, 220, 247, 277, 1360]
# data_set2 = [169, 225, 246, 268, 4138]
# data_set3 = [225, 328, 366, 412, 5872]
# data_set4 = [231, 329, 372, 425, 8193]

datasets = [
    [152, 268, 291, 317, 1497],
    [105, 214, 235, 253, 323],
    [135, 233, 254, 278, 568],
    [126, 233, 252, 272, 596],
    [129, 248, 272, 295, 588],
    [118, 226, 241, 259, 583],
    [123, 231, 258, 281, 667],
    [116, 206, 223, 249, 521],
    [92, 203, 227, 254, 548],
    [151, 213, 236, 264, 542]
]

output_file = 'fig_1-10.jpg'
y_threshold = 800  # Adjust this threshold as needed

plot_multiple_box_plots(datasets, output_file, y_threshold)
