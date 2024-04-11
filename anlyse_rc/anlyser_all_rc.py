import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import re

def read_data(file_path):
    data = {}
    errors = []

    with open(file_path, 'r') as file:
        for line in file:
            if '-nan' in line:
                errors.append(f"Error: Invalid data found in line: {line.strip()}")
                continue

            match = re.search(r"(TDC\d+_[0-9]+): rc_adjust: (0x[0-9A-F]+) heights:(.*)", line)
            if match:
                tdc_name, hex_num, heights_str = match.groups()
                try:
                    heights = [float(h) for h in heights_str.split()]
                    if len(heights) % 4 != 0:
                        errors.append(f"Error: Unexpected number of heights in line: {line.strip()}")
                        continue

                    # Split heights into groups of 4
                    grouped_heights = [heights[i:i+4] for i in range(0, len(heights), 4)]
                    if tdc_name not in data:
                        data[tdc_name] = {}
                    if hex_num not in data[tdc_name]:
                        data[tdc_name][hex_num] = []
                    data[tdc_name][hex_num].extend(grouped_heights)
                except ValueError:
                    errors.append(f"Error: Non-numeric data found in line: {line.strip()}")

    return data, errors

def calculate_std(data):
    std_devs = {}
    for tdc, hex_data in data.items():
        std_devs[tdc] = []
        for hex_num, height_groups in hex_data.items():
            for group_index, heights in enumerate(height_groups):
                if heights:
                    std_devs[tdc].append((f"{hex_num}_{group_index}", np.std(heights)))
    return std_devs

def plot_std_devs(std_devs):
    plt.figure(figsize=(14, 8))
    colors = cm.rainbow(np.linspace(0, 1, len(std_devs)))

    for (tdc, color) in zip(std_devs.keys(), colors):
        entries = std_devs[tdc]
        if not entries:
            continue

        hex_group_labels, stds = zip(*entries)
        plt.scatter(hex_group_labels, stds, label=tdc, color=color, marker='o')

    plt.xlabel('Hex Number_Group', fontsize=14)
    plt.ylabel('Standard Deviation of Heights', fontsize=14)
    plt.title('Standard Deviation vs. Hex Number for Each Module', fontsize=16)
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

# Main execution
file_path = 'result.txt'
data, errors = read_data(file_path)

# Print or log errors
for error in errors:
    print(error)

std_devs = calculate_std(data)
plot_std_devs(std_devs)
