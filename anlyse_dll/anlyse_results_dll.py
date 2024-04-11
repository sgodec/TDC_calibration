import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import re

def process_file(filepath):
    tdc_data = {}

    with open(filepath, 'r') as file:
        for line in file:
            if line.startswith("TDC"):
                parts = line.split("Heights:")
                tdc_id = parts[0].split(':')[0].strip()
                heights = np.array([float(height) for height in parts[1].split() if float(height) != 0])
                if tdc_id in tdc_data:
                    tdc_data[tdc_id].append(heights)
                else:
                    tdc_data[tdc_id] = [heights]
    return tdc_data

def calculate_mean_square_subgroups(array):

    if len(array) == 96:
        subgroup_size = 32
        num_subgroups = 3

    elif len(array) == 64:
        subgroup_size = 32
        onum_subgroups = 2

    else:
        return []
    
    mean_squares = []
    for i in range(num_subgroups):
        start_idx = i * subgroup_size
        end_idx = start_idx + subgroup_size
        subgroup = array[start_idx:end_idx]
        mean_square = np.mean(np.square(subgroup))
        mean_squares.append(mean_square)
    return mean_squares

def plot_tdc_std_devs(tdc_data):
    plt.figure(figsize=(10, 6))
    plt.rcParams['font.size'] = 12  # Increase font size
    plt.rcParams['axes.labelsize'] = 14
    plt.rcParams['axes.labelweight'] = 'bold'
    plt.rcParams['axes.titlesize'] = 16
    plt.rcParams['axes.titleweight'] = 'bold'
    plt.rcParams['xtick.labelsize'] = 12
    plt.rcParams['ytick.labelsize'] = 12
    plt.rcParams['legend.fontsize'] = 12
    plt.rcParams['figure.titlesize'] = 18
    rc('text', usetex=False)
    rc('font', family='serif')
    i = 0
    std_devs = 0
    title_id = 0
    title = ['C side module 103', 'C side module 104', 'A side module 101', 'A side module 102']
    colormap = plt.cm.plasma
    color_norm = plt.Normalize(vmin=0, vmax=(len(tdc_data)-1)//2.5)
    scalar_map = plt.cm.ScalarMappable(norm=color_norm, cmap=colormap)

    
    for tdc, heights_lists in enumerate(tdc_data.values()):
        std_devs_new = np.array([np.std(heights) for heights in heights_lists if len(heights) > 0])
        x_values = np.arange(1, len(std_devs_new) + 1)
        if i == 2:
            plt.plot(x_values, std_devs, '-o', lw=2, color=scalar_map.to_rgba(title_id), label=title[title_id], markersize=8)
            i = 0
            std_devs = 0
            title_id += 1
        else:
            std_devs = std_devs + std_devs_new if std_devs is not 0 else std_devs_new
            i += 1

    plt.xlabel('Iteration Step of Algorithm')
    plt.ylabel('Standard Deviation of Occupancy for DLL')
    plt.title('Standard Deviation of Occupancy as Function of Iterative Step for HPTDC Module')
    plt.legend()
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()  # Adjust layout to make room for the larger text
    plt.show()
#def plot_tdc_std_devs(tdc_data):
#    plt.figure(figsize=(10, 6))
#    i = 0
#    std_devs = 0
#    title_id = 0
#    title = ['C side module 103','C side module 104','A side module 101','A side module 102']
#    for tdc, heights_lists in tdc_data.items():
#        std_devs_new = np.array([np.std(heights) for heights in heights_lists if len(heights) > 0])
#        x_values = np.arange(1, len(std_devs_new) + 1)
#        if i == 2:
#            plt.plot(x_values, std_devs, '-o', lw = 2,label=title[title_id])
#            i = 0
#            std_devs = 0
#            title_id += 1
#        else:
#            std_devs = std_devs + std_devs_new
#            i += 1
#    plt.xlabel('Iteration step of algorithm')
#    plt.ylabel('Standard deviation of occupancy fo Dll ')
#    plt.title('Standard deviation of occupancy as funciton of iterative step for HPTDC module')
#    plt.legend()
#    plt.grid(True)
#    plt.show()

def plot_dnl_subgroups_for_selected_tdcs(tdc_data):
    tdc_groups = [
        ('TDC1_101', 'TDC2_101', 'TDC1_103', 'TDC1_102', 'TDC2_102', 'TDC3_102'),
        ('TDC1_103', 'TDC2_103', 'TDC3_103', 'TDC1_104', 'TDC2_104', 'TDC3_104')
    ]
    tdc_title = ['T3_BC', 'T1_BA', 'T1_BD', 'T3_BB', 'T1_BC','T3_BA', 'T3_BD','T1_BB', 'T2_BC', 'T0_BA', 'T0_BD','T2_BB', 'T0_BC','T2_BA','T2_BD','T0_BB']
    group_titles = ['C Side', 'A Side'] 
    colors = ['darkgreen', 'darkred']  

    def calculate_dnl(subgroup):
        mean_height = np.mean(subgroup)
        return (subgroup - mean_height) / mean_height if mean_height != 0 else subgroup * 0
    for idx, group in enumerate(tdc_groups):
        fig, axs = plt.subplots(4, 4, figsize=(20, 15), constrained_layout=False)
        fig.suptitle(group_titles[idx], fontsize=20)
        subplot_idx = 0 
        for tdc in group:
            heights_lists = tdc_data[tdc]
            overall_std_devs = [np.std(heights) for heights in heights_lists]
            best_condition_idx = np.argmin(overall_std_devs)
            worst_condition_idx = np.argmax(overall_std_devs)
            best_heights = heights_lists[best_condition_idx]
            worst_heights = heights_lists[worst_condition_idx]
            num_subgroups = len(best_heights) // 32
            for i in range(num_subgroups):
                worst_subgroup = worst_heights[i*32:(i+1)*32]
                best_subgroup = best_heights[i*32:(i+1)*32]
                dnl_best = calculate_dnl(best_subgroup)
                dnl_worst = calculate_dnl(worst_subgroup)
                ax = axs[subplot_idx // 4, subplot_idx % 4]
                ax.plot(np.arange(1, 33), dnl_best, color=colors[0], linestyle='-', label='Best', linewidth=2)
                ax.plot(np.arange(1, 33), dnl_worst, color=colors[1], linestyle='--', label='Initial', linewidth=2)
                ax.set_title(f'{tdc_title[(subplot_idx) %16 ]}')
                if subplot_idx % 4 == 0: 
                    ax.set_ylabel('DNL (lsb of dll)')
                if subplot_idx // 4 == 3: 
                    ax.set_xlabel('DLL bin')
                ax.grid(True, which='both', linestyle='--', linewidth=0.5)
                ax.legend(loc='best')

                subplot_idx += 1 

        plt.tight_layout()
        plt.show()

#filepath = 'results_dll.txt.best1'  
filepath = 'results_dll_fast.txt'  
tdc_data = process_file(filepath)
print(tdc_data)
plot_tdc_std_devs(tdc_data)
#plot_dnl_subgroups_for_selected_tdcs(tdc_data)
rc('text', usetex=False)
rc('font', family='serif')
colors = ['#1f77b4', 'darkred']

def calculate_dnl(subgroup):
    mean_height = np.mean(subgroup)
    return (subgroup - mean_height) / mean_height if mean_height != 0 else subgroup * 0

def plot_dnl_subgroups_for_selected_tdcs(tdc_data):
    tdc_groups = [
        ('TDC1_101', 'TDC2_101', 'TDC1_103', 'TDC1_102', 'TDC2_102', 'TDC3_102'),
        ('TDC1_103', 'TDC2_103', 'TDC3_103', 'TDC1_104', 'TDC2_104', 'TDC3_104')]

    tdc_title = ['Train3BarC', 'Train1BarA', 'Train1BarD', 'Train3BarB', 'Train1BarC','Train3BarA', 'Train3BarD','Train1BarB', 'Train2BarC', 'Train0BarA', 'Train0BarD','Train2BarB', 'Train0BarC','Train2BarA','Train2BarD','Train0BarB']
    group_titles = ['A Side Module 101 Chip 1 DLL calibration', 'A Side Module 101 Chip 2 DLL calibration', 'A Side Module 101 Chip 3 DLL calibration','A Side Module 102 Chip 1 DLL calibration', 'A Side Module 102 Chip 2 DLL calibration', 'A Side Module 102 Chip 3 DLL calibration','C Side Module 103 Chip 1 DLL calibration', 'C Side Module 103 Chip 2 DLL calibration', 'C Side Module 103 Chip 3 DLL calibration','C Side Module 104 Chip 1 DLL calibration','C Side Module 104 Chip 2 DLL calibration', 'C Side Module 104 Chip 3 DLL calibration']

    id = 0
    for idx, group in enumerate(tdc_groups):
        subplot_idx = 0
        for tdc in group:
            heights_lists = tdc_data[tdc]
            overall_std_devs = [np.std(heights) for heights in heights_lists]
            best_condition_idx = np.argmin(overall_std_devs)
            worst_condition_idx = np.argmax(overall_std_devs)
            best_heights = heights_lists[best_condition_idx]
            worst_heights = heights_lists[worst_condition_idx]
            num_subgroups = len(best_heights) // 32
            if num_subgroups == 3:
                fig, axs = plt.subplots(1,num_subgroups, figsize=(2.3*24/3, 2.3/3*8), constrained_layout=False)
                print('trica')
            else:
                fig, axs = plt.subplots(1,num_subgroups, figsize=(2*24/3, 2/3*12), constrained_layout=False)
            fig.suptitle(group_titles[id], fontsize=21, fontweight='bold')
            fig.text(0.515, 0.013, 'DLL bin', ha='center', va='center', fontsize=12)
            for i in range(num_subgroups):
                worst_subgroup = worst_heights[i*32:(i+1)*32]
                best_subgroup = best_heights[i*32:(i+1)*32]
                bar_width = 0.45 
                ax = axs[i]
                ax.bar(np.arange(0, 32)- bar_width / 2, worst_subgroup, bar_width,color=colors[1], alpha = 0.85, label='Initial')
                ax.bar(np.arange(0, 32) + bar_width / 2, best_subgroup, bar_width,color=colors[0], alpha = 0.80, label='Best')
                ax.set_ylim([0.027,0.045])
                ax.set_title(f'{tdc_title[subplot_idx]}', fontsize=12, fontweight='bold')
                ax.tick_params(axis='both', which='major', labelsize=12)
                ax.hlines(y=1/32, xmin=-0.45, xmax=31.45, linewidth=2,linestyle = '--', color='black',label = 'Ideal')
                if i == 0:
                    ax.set_ylabel('Bin occupancy', fontsize=12)
                ax.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)
                ax.legend(loc='best', fontsize=10)
                subplot_idx += 1
            plt.tight_layout()
            plt.savefig(f'{group_titles[id].replace(" ","_")}')
            id += 1
plot_dnl_subgroups_for_selected_tdcs(tdc_data)
