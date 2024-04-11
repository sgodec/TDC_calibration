import os
import subprocess
import numpy as np

def read_heights(filename):
    desired_length = 96
    with open(filename, 'r') as file:
        arrays = [np.array(line.strip().split(), dtype=float) for line in file]
    padded_arrays = [np.pad(arr, (0, max(0, desired_length - len(arr))), mode='constant', constant_values=0) for arr in arrays]
    heights = np.vstack(padded_arrays)
    return heights

def initialize_dll_tap_matrices(num_tdcs=12, length=32, initial_value=4):
    return np.full((num_tdcs, length), initial_value, dtype=int)

def apply_algorithm(heights, dll_tap, index,step):
    dll_tap_updated = np.copy(dll_tap)
    alpha = 0.0015
    for i in range(heights.shape[0]):
        # Step 1: Sum groups
        summed_array = np.roll(np.array([heights[i, j] + heights[i, j+32] + heights[i, j+64] for j in range(32)]),shift=5)
        
        average = np.mean(summed_array)
        # Step 2: Shift left and subtract
        
        difference_array = summed_array - average  
        if difference_array[index] > alpha:
            dll_tap_updated[i,index] =  dll_tap[i,index] - step  
        elif difference_array[index] < - alpha: 
            dll_tap_updated[i,index] =  dll_tap[i,index] + step  
        else:
            pass
        dll_tap_updated[i, :] = np.clip(dll_tap_updated[i, :], 0, 7)
    return dll_tap_updated

def write_results(heights, dll_tap, output_filename):
    tdcs = ['TDC1_103', 'TDC2_103', 'TDC3_103', 'TDC1_104', 'TDC2_104', 'TDC3_104', 'TDC1_101', 'TDC2_101', 'TDC3_101', 'TDC1_102', 'TDC2_102', 'TDC3_102']
    with open(output_filename, 'a') as file:
        for i, height_array in enumerate(heights):
            dll_tap_str = ' '.join(map(str, dll_tap[i]))
            height_str = ' '.join(map(str, height_array))
            file.write(f"{tdcs[i]}: DLL Tap: {dll_tap_str} Heights: {height_str}\n")

def update_tdc_configuration(dll_tap):
    real_dll_tap = dll_tap
    
    config = {'103': 113, '104': 109, '101': 113, '102': 108}
    for k, name in enumerate(config.keys()):
        k = 3 * k
        i = config[name]
        config_filename = f'/det/afp/configs/moduleconfigs/afp-hptdc/configs/HPTDC{name}-i2c.cfg'
        
        line_numbers = [0+i, 1+i, 2+i, 3+i, 4+i, 5+i, 6+i, 7+i]

        with open(config_filename, 'r') as file:
            lines = file.readlines()

        for j, line_num in enumerate(line_numbers):
            start_index = j * 4
            end_index = start_index + 4
            
            binary_str_0 = ''.join([format(val, 'b').zfill(3) for val in real_dll_tap[k,start_index:end_index][::-1]])
            hex_str_0 = format(int(binary_str_0, 2), 'x').upper().zfill(3)
            
            # Check to ensure k+1 and k+2 are within bounds
            if k+1 < len(dll_tap) and k+2 < len(dll_tap):
                binary_str_1 = ''.join([format(val, 'b').zfill(3) for val in real_dll_tap[k+1,start_index:end_index][::-1]])
                hex_str_1 = format(int(binary_str_1, 2), 'x').upper().zfill(3)
                binary_str_2 = ''.join([format(val, 'b').zfill(3) for val in real_dll_tap[k+2,start_index:end_index][::-1]])
                hex_str_2 = format(int(binary_str_2, 2), 'x').upper().zfill(3)
            else:
                continue

            new_line = f'dll_tap_adjust{end_index-1}_{start_index}                         0x{hex_str_0} 0x{hex_str_1} 0x{hex_str_2}\n'
            lines[line_num] = new_line

        with open(config_filename, 'w') as file:
            file.writelines(lines)

def main():
    output_filename = 'results_dll.txt'
    heights_filename = 'heights.txt'
    dll_tap = initialize_dll_tap_matrices()
    dll_tap = np.array([[0,0,2,2,2,4,6,6,7,7,7,7,7,7,7,7,7,6,7,6,6,7,7,7,7,7,7,7,6,7,7,6],[0,0,0,0,2,4,4,6,7,7,7,6,6,6,6,7,7,7,7,6,6,6,6,7,6,7,7,7,7,6,7,6],[0,0,0,0,0,0,2,2,2,2,2,2,2,4,6,6,6,6,6,6,6,6,6,4,4,5,4,5,4,4,4,4],[0,0,2,2,2,4,4,6,6,6,6,6,6,7,7,7,6,6,6,7,6,6,7,6,7,6,7,7,6,4,4,4],[0,0,0,0,0,2,2,2,2,4,4,4,4,4,4,6,6,6,6,6,7,7,7,7,7,6,7,7,7,6,6,6],[0,0,0,2,2,4,4,4,4,6,6,6,6,6,6,6,6,7,7,6,6,6,7,7,7,7,7,7,7,7,7,4],[0,0,2,2,2,2,2,2,4,6,6,6,6,6,6,6,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],[0,0,0,2,2,4,4,4,5,4,4,5,5,5,4,4,5,5,5,5,4,5,5,5,5,5,5,4,5,4,5,5],[0,0,0,2,2,2,4,4,4,4,4,4,4,6,6,7,7,6,7,7,7,6,7,7,7,7,7,7,7,7,7,7],[0,0,2,2,2,2,2,2,6,6,6,4,6,6,6,4,4,4,4,4,2,4,4,5,5,5,4,4,5,5,5,5],[0,0,2,2,2,4,2,2,4,6,6,7,7,6,7,7,7,7,7,6,7,6,7,6,7,6,4,4,4,4,4,4],[0,0,0,2,2,2,2,2,4,4,2,2,2,2,4,4,5,5,5,5,5,5,5,4,5,5,5,5,5,5,5,5]])
    dll_tap = np.array([[1, 0, 1, 2, 2, 3, 4, 3, 5, 5, 4, 4, 4, 3, 3, 4, 4, 3, 5, 5, 4, 5, 5, 7, 6, 6, 7, 7, 6, 7, 7, 7], [0, 0, 1, 0, 2, 4, 3, 3, 4, 4, 4, 3, 4, 4, 3, 4, 5, 5, 5, 3, 3, 3, 2, 4, 3, 4, 4, 4, 5, 5, 7, 7], [0, 0, 1, 1, 2, 2, 4, 4, 4, 4, 2, 3, 4, 5, 5, 3, 3, 5, 4, 3, 4, 4, 5, 5, 4, 6, 5, 6, 5, 5, 6, 7], [1, 0, 1, 0, 1, 3, 3, 6, 6, 5, 5, 5, 3, 5, 5, 5, 3, 4, 2, 4, 3, 3, 5, 4, 6, 5, 6, 7, 7, 6, 7, 7], [1, 0, 1, 2, 2, 4, 4, 4, 4, 5, 6, 5, 5, 4, 4, 5, 6, 6, 5, 4, 4, 4, 5, 5, 5, 4, 4, 4, 5, 5, 6, 7], [1, 0, 1, 1, 1, 3, 5, 5, 6, 6, 6, 6, 5, 5, 5, 6, 5, 6, 5, 3, 3, 2, 5, 5, 6, 6, 6, 7, 7, 7, 7, 7], [2, 0, 1, 2, 3, 4, 5, 4, 7, 7, 6, 5, 6, 6, 5, 6, 6, 6, 5, 5, 5, 5, 5, 6, 6, 6, 5, 6, 6, 6, 7, 7], [1, 0, 1, 2, 2, 3, 4, 3, 4, 3, 3, 4, 4, 4, 3, 4, 5, 5, 5, 4, 2, 3, 4, 4, 4, 4, 4, 3, 5, 4, 6, 7], [0, 0, 0, 1, 2, 3, 5, 5, 5, 4, 4, 4, 3, 4, 3, 5, 5, 3, 3, 4, 4, 3, 4, 6, 6, 6, 5, 7, 7, 7, 7, 7], [1, 0, 1, 1, 2, 4, 4, 3, 6, 5, 5, 2, 4, 3, 4, 3, 4, 5, 5, 5, 3, 5, 5, 7, 7, 7, 6, 6, 7, 6, 6, 7], [2, 0, 2, 3, 2, 4, 2, 2, 4, 5, 4, 5, 4, 3, 3, 4, 4, 3, 4, 3, 5, 4, 5, 3, 4, 3, 3, 5, 6, 6, 7, 7], [0, 0, 2, 3, 4, 4, 4, 4, 5, 5, 5, 6, 5, 4, 4, 4, 4, 5, 4, 3, 4, 4, 3, 2, 3, 4, 4, 5, 6, 6, 6, 7]])
    update_tdc_configuration(dll_tap)
    subprocess.run(['bash', 'ttc_gnam_reset.sh'])
    subprocess.run(['bash', 'read_heights_dll.sh'])
    for iteration in range(15):
        for i in range(32): 
            heights = read_heights(heights_filename)
            write_results(heights, dll_tap, output_filename)
            print(np.array([np.std(row[row > 0]) for row in heights]))
            print(f"Results written to {output_filename}")
            dll_tap = apply_algorithm(heights, dll_tap,i,1)
            update_tdc_configuration(dll_tap)
            #TTC reset and update of gnam
            subprocess.run(['bash', 'ttc_gnam_reset.sh'])
            subprocess.run(['bash', 'read_heights_dll.sh'])
            #print sigma
if __name__ == "__main__":
    main()
