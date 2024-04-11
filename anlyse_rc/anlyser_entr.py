import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import re

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

def calculate_grouped_entropy(data):
    entropy_values = {}
    for tdc, hex_data in data.items():
        for hex_num, heights in hex_data.items():
            if not heights:
                continue

            num_heights = len(heights)
            entropies = []

            def entropy(heights):
                total = sum(heights)
                if total == 0:
                    return 0
                probabilities = [h / total for h in heights]
                return -sum(p * np.log2(p) for p in probabilities if p > 0)

            if num_heights >= 4:
                entropies.append(entropy(heights[0:4]))
            if num_heights >= 8:
                entropies.append(entropy(heights[4:8]))
            if num_heights == 12:
                entropies.append(entropy(heights[8:12]))

            avg_entropy = np.mean(entropies) if entropies else 0

            if tdc not in entropy_values:
                entropy_values[tdc] = {}
            entropy_values[tdc][hex_num] = avg_entropy

    return entropy_values

def plot_entropy_values(entropy_values):
    plt.figure(figsize=(14, 8))
    colors = cm.rainbow(np.linspace(0, 1, len(entropy_values)))

    for tdc, color in zip(entropy_values.keys(), colors):
        hex_nums = list(entropy_values[tdc].keys())
        hex_nums.sort(key=lambda x: int(x, 16))  # Sorting hex numbers numerically

        entropies = [entropy_values[tdc][hex_num] for hex_num in hex_nums]
        plt.scatter(hex_nums, entropies, label=tdc, color=color, marker='o')

    plt.xlabel('Hex Number', fontsize=14)
    plt.ylabel('Average Entropy of Heights', fontsize=14)
    plt.title('Average Entropy vs. Hex Number for Each TDC', fontsize=16)
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
def find_max_entropy_hex(entropy_values):
    max_entropy_hex = {}
    for tdc, hex_data in entropy_values.items():
        max_entropy = -1
        max_hex = None
        for hex_num, entropy in hex_data.items():
            if entropy > max_entropy:
                max_entropy = entropy
                max_hex = hex_num
        max_entropy_hex[tdc] = max_hex
    return max_entropy_hex
def plot_final_heights(data, max_entropy_hex):
    plt.figure(figsize=(14, 8))
    colors = cm.rainbow(np.linspace(0, 1, len(max_entropy_hex)))

    for (tdc, hex_num), color in zip(max_entropy_hex.items(), colors):
        heights = data[tdc][hex_num]
        plt.plot(heights, label=f"{tdc} - {hex_num}", color=color, marker='o')

    plt.xlabel('Index', fontsize=14)
    plt.ylabel('Heights', fontsize=14)
    plt.title('Final Heights for Best Hex Numbers', fontsize=16)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

file_path = 'result.txt'
data = read_data(file_path)
grouped_entropies = calculate_grouped_entropy(data)
max_entropy_hex = find_max_entropy_hex(grouped_entropies)
for tdc, hex_num in max_entropy_hex.items():
    print(f"{tdc} - Max Entropy Hex: {hex_num}")

plot_entropy_values(grouped_entropies)
plot_final_heights(data, max_entropy_hex)

