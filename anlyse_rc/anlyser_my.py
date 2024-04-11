import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import re
import matplotlib as mpl
mpl.style.use("Kouristyle.mplstyle")
def read_data(file_path):
    data = {}
    with open(file_path, 'r') as file:
        for line in file:
            if 'nan' in line:
                continue  # Skip lines with 'nan'

            match = re.search(r"(TDC\d+_\d+):\s+rc_adjust:\s+(0x[0-9A-F]+)\s+heights:(.*)", line.strip())
            if match:
                tdc_name, hex_num, heights_str = match.groups()
                try:
                    heights = [float(h) for h in heights_str.split() if h]
                    if tdc_name not in data:
                        data[tdc_name] = {}
                    data[tdc_name][hex_num] = heights
                except ValueError:
                    continue  # Skip lines with parsing errors
    return data

def calculate_grouped_std(data):
    std_devs = {}
    for tdc, hex_data in data.items():
        for hex_num, heights in hex_data.items():
            if not heights:
                continue

            num_heights = len(heights)
            stds = []

            if num_heights >= 4:
                stds.append(np.std(heights[0:4]))
            if num_heights >= 8:
                stds.append(np.std(heights[4:8]))
            if num_heights == 12:
                stds.append(np.std(heights[8:12]))

            avg_std = np.mean(stds) if stds else 0

            if tdc not in std_devs:
                std_devs[tdc] = {}
            std_devs[tdc][hex_num] = avg_std

    return std_devs
def plot_std_devs(std_devs):
    plt.figure(figsize=(14, 8))
    colors = cm.rainbow(np.linspace(0, 1, len(std_devs)))

    for tdc, color in zip(std_devs.keys(), colors):
        # Extract and sort hex numbers in numerical order
        hex_nums = list(std_devs[tdc].keys())
        hex_nums.sort(key=lambda x: int(x, 16))  # Sorting hex numbers numerically

        stds = [std_devs[tdc][hex_num] for hex_num in hex_nums]
        plt.scatter(hex_nums, stds, label=tdc, color=color, marker='o')

    plt.xlabel('Hex Number', fontsize=14)
    plt.ylabel('Average Standard Deviation of Heights', fontsize=14)
    plt.title('Average Standard Deviation vs. Hex Number for Each TDC', fontsize=16)
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
def find_max_std_hex(std_devs):
    max_std_hex = {}
    for tdc, hex_data in std_devs.items():
        max_std = 100
        max_hex = None
        for hex_num, std in hex_data.items():
            if std < max_std:
                max_std = std
                max_hex = hex_num
        max_std_hex[tdc] = max_hex
    return max_std_hex
# Main execution
file_path = 'result.txt'
data = read_data(file_path)
grouped_stds = calculate_grouped_std(data)
grouped_stds = calculate_grouped_std(data)
min_std_hex = find_max_std_hex(grouped_stds)

# Print the hex number with the highest standard deviation for each TDC
for tdc, hex_num in min_std_hex.items():
    print(f"{tdc} - min Std Hex: {hex_num}")

plot_std_devs(grouped_stds)
