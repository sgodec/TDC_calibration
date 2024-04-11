import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import re
import matplotlib as mpl
mpl.style.use("Kouristyle.mplstyle")

def read_data(file_path):
    data = {}
    errors = []

    with open(file_path, 'r') as file:
        for line in file:
            if '-nan' in line or 'nan' in line:
                errors.append(f"Error: Invalid data found in line: {line.strip()}")
                continue

            # Updated regex pattern
            match = re.search(r"(TDC\d+_\d+):\s+rc_adjust:\s+(0x[0-9A-F]+)\s+heights:(.*)", line.strip())
            if match:
                tdc_name, hex_num, heights_str = match.groups()
                try:
                    # Filter out any empty strings after splitting
                    heights = [float(h) for h in heights_str.split() if h]
                    if tdc_name not in data:
                        data[tdc_name] = {}
                    if hex_num not in data[tdc_name]:
                        data[tdc_name][hex_num] = []
                    data[tdc_name][hex_num].extend(heights)
                except ValueError as e:
                    errors.append(f"Error parsing heights in line: {line.strip()}")
                    continue
    return data, errors
def calculate_std(data):
    std_devs = {}
    for tdc, hex_data in data.items():
        for hex_num, heights in hex_data.items():
            if not heights:
                continue

            # Splitting the heights into chunks of 4
            chunks = [heights[i:i + 4] for i in range(0, len(heights), 4)]
            
            # Calculate standard deviation for each chunk
            stds = [np.std(chunk) for chunk in chunks if chunk]
            
            # Calculate the average of these standard deviations
            avg_std = np.mean(stds) if stds else 0

            if tdc not in std_devs:
                std_devs[tdc] = []
            std_devs[tdc].append((hex_num, avg_std))
    return std_devs

def plot_std_devs(std_devs):
    plt.figure(figsize=(14, 8))
    colors = cm.plasma(np.linspace(0, 1, len(std_devs)))

    for (tdc, color) in zip(std_devs.keys(), colors):
        entries = std_devs[tdc]
        if not entries:
            continue
        hex_nums, stds = zip(*entries)
        plt.scatter(hex_nums, stds, label=tdc, color=color, marker='o')

    plt.xlabel('Hex Number', fontsize=14)
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

std_devs = calculate_std(data)
total_hex_numbers = sum(len(std_devs[tdc]) for tdc in std_devs)
print(f"Total hex numbers plotted: {total_hex_numbers}")

plot_std_devs(std_devs)
