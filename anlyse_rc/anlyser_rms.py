import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import re

def read_data(file_path):
    data = {}
    with open(file_path, 'r') as file:
        for line in file:
            if 'nan' in line:
                continue
            match = re.search(r"(TDC\d+_\d+):\s+rc_adjust:\s+(0x[0-9A-F]+)\s+heights:(.*)", line.strip())
            if match:
                tdc_name, hex_num, heights_str = match.groups()
                try:
                    heights = [float(h) for h in heights_str.split() if h]
                    if tdc_name not in data:
                        data[tdc_name] = {}
                    data[tdc_name][hex_num] = heights
                except ValueError:
                    continue
    return data

def calculate_grouped_rms(data):
    rms_values = {}
    for tdc, hex_data in data.items():
        for hex_num, heights in hex_data.items():
            if not heights:
                continue
            rms = np.sqrt(np.mean(np.square(heights)))
            if tdc not in rms_values:
                rms_values[tdc] = {}
            rms_values[tdc][hex_num] = rms
    return rms_values

def find_min_rms_hex(rms_values):
    min_rms_hex = {}
    for tdc, hex_data in rms_values.items():
        min_rms = float('inf')
        min_hex = None
        for hex_num, rms in hex_data.items():
            if rms < min_rms:
                min_rms = rms
                min_hex = hex_num
        min_rms_hex[tdc] = min_hex
    return min_rms_hex

def find_max_rms_hex(rms_values):
    max_rms_hex = {}
    for tdc, hex_data in rms_values.items():
        max_rms = -float('inf')
        max_hex = None
        for hex_num, rms in hex_data.items():
            if rms > max_rms:
                max_rms = rms
                max_hex = hex_num
        max_rms_hex[tdc] = max_hex
    return max_rms_hex

# Main execution
file_path = 'result.txt'
data = read_data(file_path)
rms_values = calculate_grouped_rms(data)
min_rms_hex = find_min_rms_hex(rms_values)
max_rms_hex = find_max_rms_hex(rms_values)

for tdc, hex_num in min_rms_hex.items():
    print(f"{tdc} - Min RMS Hex: {hex_num}")

rc('text', usetex=False)
rc('font', family='serif', size=12)

colors = ['#1f77b4', 'darkred']  


def plot_heights_for_min_rms(data, min_rms_hex, max_rms_hex):

    tdc_groups = [
        ('TDC1_101', 'TDC2_101', 'TDC1_103', 'TDC1_102', 'TDC2_102', 'TDC3_102'),
        ('TDC1_103', 'TDC2_103', 'TDC3_103', 'TDC1_104', 'TDC2_104', 'TDC3_104')
    ]
    tdc_title = ['Train3BarC', 'Train1BarA', 'Train1BarD', 'Train3BarB', 'Train1BarC','Train3BarA', 'Train3BarD','Train1BarB', 'Train2BarC', 'Train0BarA', 'Train0BarD','Train2BarB', 'Train0BarC','Train2BarA','Train2BarD','Train0BarB']

    group_titles = ['A Side Module 101 Chip 1 RC calibration', 'A Side Module 101 Chip 2 RC calibration', 'A Side Module 101 Chip 3 RC calibration','A Side Module 102 Chip 1 RC calibration', 'A Side Module 102 Chip 2 RC calibration', 'A Side Module 102 Chip 3 RC calibration','C Side Module 103 Chip 1 RC calibration', 'C Side Module 103 Chip 2 RC calibration', 'C Side Module 103 Chip 3 RC calibration','C Side Module 104 Chip 1 RC calibration','C Side Module 104 Chip 2 RC calibration', 'C Side Module 104 Chip 3 RC calibration']

    id = 0

    for idx, group in enumerate(tdc_groups):
        subplot_idx = 0
        for tdc in group:
            best_hex = min_rms_hex[tdc]
            worst_hex = max_rms_hex[tdc]
            best_heights = data[tdc][best_hex]
            worst_heights = data[tdc][worst_hex]
            num_sets = len(best_heights) // 4 

            bar_width = 0.35  
            bins = np.array([0, 1, 2, 3])  

            if num_sets == 3:
                fig, axs = plt.subplots(1,num_sets, figsize=(2*24/3, 2/3*8), constrained_layout=False)
                print('three')
            else:    
                fig, axs = plt.subplots(1,num_sets, figsize=(2*24/3,2/3 * 12), constrained_layout=False)

            fig.suptitle(group_titles[id], fontsize=20, fontweight='bold')

            fig.text(0.515, 0.013, 'RC bin', ha='center', va='center', fontsize=12)

            for set_num in range(num_sets):
                best_heights_final = best_heights[set_num*4:(set_num+1)*4]
                worst_heights_final = worst_heights[set_num*4:(set_num+1)*4]
                ax = axs[set_num]

                ax.bar(bins - bar_width / 2, worst_heights_final, bar_width, color=colors[1], label='Initial', alpha = 0.80)

                ax.bar(bins + bar_width / 2, best_heights_final, bar_width, color=colors[0], label='Best',alpha =0.85)

                ax.set_title(f'{tdc_title[subplot_idx]}', fontsize=14, fontweight='bold')

                if set_num == 0:
                    ax.set_ylabel('Bin occupancy', fontsize=12)
                    o
                ax.hlines(y=0.98/4, xmin=-0.35, xmax=3.35, linewidth=2,linestyle = '--', color='black',label = 'Ideal')

                ax.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)
                ax.set_ylim([0, 0.8])
                ax.legend(loc='best', fontsize=10)
                subplot_idx += 1

            plt.tight_layout()
            plt.savefig(f'{group_titles[id].replace(" ", "_" )}')
            id += 1

plot_heights_for_min_rms(data, min_rms_hex, max_rms_hex)
