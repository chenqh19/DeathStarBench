import matplotlib.pyplot as plt
import numpy as np

def plot_multiple_box_plots(data_sets, output_file, y_threshold):
    fig, ax = plt.subplots(figsize=(5, 6))
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
    ax.set_xticklabels(["1-node\n10k posts", "1-node\n200k posts", "2-node\n10k posts", "2-node\n200k posts"])
    ax.set_ylabel('Remote function call overhead')

    # Customize box colors
    colors = ['lightblue', 'lightblue', 'lightgreen', 'lightgreen']
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

    plt.title('HomeTimeline calls Read_Post')
    plt.savefig(output_file)
    plt.show()

# Example usage with multiple data sets
data_set1 = [96, 220, 247, 277, 1360]
data_set2 = [169, 225, 246, 268, 4138]
data_set3 = [225, 328, 366, 412, 5872]
data_set4 = [231, 329, 372, 425, 8193]

output_file = 'fig_vertical_with_threshold.jpg'
y_threshold = 500  # Adjust this threshold as needed

plot_multiple_box_plots([data_set1, data_set2, data_set3, data_set4], output_file, y_threshold)
