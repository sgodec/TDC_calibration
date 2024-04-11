import numpy as np
import os
import subprocess

def read_heights(filename):
    desired_length = 96
    with open(filename, 'r') as file:
        arrays = [np.array(line.strip().split(), dtype=float) for line in file]
    padded_arrays = [np.pad(arr, (0, max(0, desired_length - len(arr))), mode='constant', constant_values=0) for arr in arrays]
    heights = np.vstack(padded_arrays)
    return heights

def initialize_dll_tap_matrices(num_tdcs=12, length=32, initial_value=4):
    if initial_value is None:  
        return np.full((num_tdcs, length), 4, dtype=int)  + np.random.randint(-1, 2, size=(num_tdcs, length))
    else:  # Use a fixed initial value
        return np.full((num_tdcs, length), initial_value, dtype=int)

def perturbate(dll_tap,num_tdcs=12, length=32):
    return np.clip(dll_tap + np.random.randint(-2, 3, size=(num_tdcs, length)),0,7)

def apply_and_evaluate_changes(heights_filename, dll_tap):
    update_tdc_configuration(np.roll(dll_tap,shift=5,axis = 1))
    subprocess.run(['bash', 'ttc_gnam_reset.sh'])
    subprocess.run(['bash', 'read_heights_dll.sh']) # Fetch new measurements
    new_heights = read_heights(heights_filename)
    write_results(new_heights,np.roll(dll_tap,shift=5,axis = 1), 'results_dll_slow.txt')
    new_heights_std = np.array([np.std(row[row > 0]) for row in new_heights])
    return new_heights_std
1
def optimize_dll_tap(heights_filename, dll_tap,step=1):
    
    best_std = apply_and_evaluate_changes(heights_filename, dll_tap)
    for col_index in range(dll_tap.shape[1]):
        original_values = dll_tap[:, col_index].copy()

        # Try increasing
        dll_tap[:, col_index] = np.clip(original_values + step, 0, 7)
        increased_std = apply_and_evaluate_changes(heights_filename, dll_tap)
        increase_improvement = best_std - increased_std

        # Try decreasing
        dll_tap[:, col_index] = np.clip(original_values - step, 0, 7)
        decreased_std = apply_and_evaluate_changes(heights_filename, dll_tap)
        decrease_improvement = best_std - decreased_std

        # Evaluate improvements and adjust the tap settings
        for row_index in range(dll_tap.shape[0]):
            if increase_improvement[row_index] > 0 and decrease_improvement[row_index] > 0:
                if increase_improvement[row_index] > decrease_improvement[row_index]:
                    dll_tap[row_index, col_index] = np.clip(original_values[row_index] + step, 0, 7)
                    best_std[row_index] = increased_std[row_index]
                else:
                    dll_tap[row_index, col_index] = np.clip(original_values[row_index] - step, 0, 7)
                    best_std[row_index] = decreased_std[row_index]
            elif increase_improvement[row_index] > 0:
                dll_tap[row_index, col_index] = np.clip(original_values[row_index] + step, 0, 7)
                best_std[row_index] = increased_std[row_index]
            elif decrease_improvement[row_index] > 0:
                dll_tap[row_index, col_index] = np.clip(original_values[row_index] - step, 0, 7)
                best_std[row_index] = decreased_std[row_index]
            else:
                # No improvement, so revert to the original value
                dll_tap[row_index, col_index] = original_values[row_index]
    return dll_tap

def write_results(heights, dll_tap, output_filename):
    tdcs = ['TDC1_103', 'TDC2_103', 'TDC3_103', 'TDC1_104', 'TDC2_104', 'TDC3_104', 'TDC1_101', 'TDC2_101', 'TDC3_101', 'TDC1_102', 'TDC2_102', 'TDC3_102']
    with open(output_filename, 'a') as file:
        for i, height_array in enumerate(heights):
            dll_tap_str = ' '.join(map(str, dll_tap[i]))
            height_str = ' '.join(map(str, height_array))
            file.write(f"{tdcs[i]}: DLL Tap: {dll_tap_str} Heights: {height_str}\n")

def update_tdc_configuration(dll_tap):
    config = {'103': 113, '104': 109, '101': 113, '102': 108}
    for k, name in enumerate(config.keys()):
        k = k*3
        i = config[name]
        config_filename = f'/det/afp/configs/moduleconfigs/afp-hptdc/configs/HPTDC{name}-i2c.cfg'
        line_numbers = [0+i, 1+i, 2+i, 3+i, 4+i, 5+i, 6+i, 7+i]

        with open(config_filename, 'r') as file:
            lines = file.readlines()

        for j, line_num in enumerate(line_numbers):
            start_index = j * 4
            end_index = start_index + 4
            
            binary_str_0 = ''.join([format(val, 'b').zfill(3) for val in dll_tap[k,start_index:end_index][::-1]])
            hex_str_0 = format(int(binary_str_0, 2), 'x').upper().zfill(3)
            
            # Check to ensure k+1 and k+2 are within bounds
            if k+1 < len(dll_tap) and k+2 < len(dll_tap):
                binary_str_1 = ''.join([format(val, 'b').zfill(3) for val in dll_tap[k+1,start_index:end_index][::-1]])
                hex_str_1 = format(int(binary_str_1, 2), 'x').upper().zfill(3)
                binary_str_2 = ''.join([format(val, 'b').zfill(3) for val in dll_tap[k+2,start_index:end_index][::-1]])
                hex_str_2 = format(int(binary_str_2, 2), 'x').upper().zfill(3)
            else:
                continue  # Skip updating this line if k+1 or k+2 are out of bounds

            new_line = f'dll_tap_adjust{end_index-1}_{start_index}                         0x{hex_str_0} 0x{hex_str_1} 0x{hex_str_2}\n'
            lines[line_num] = new_line

        with open(config_filename, 'w') as file:
            file.writelines(lines)
def main():
    output_filename = 'results_dll_slow.txt'
    heights_filename = 'heights.txt'
    iteration_count = 6

    dll_tap = initialize_dll_tap_matrices(12,32,None) 
    #dll_tap = np.array([[7, 5, 6, 4, 3, 3, 5, 4, 4, 3, 4, 1, 3, 3, 5, 4, 3, 6, 5, 4, 2, 5, 2, 4, 3, 6, 3, 5, 5, 2, 0, 2],[7, 7, 4, 5, 6, 4, 5, 5, 4, 4, 3, 4, 3, 4, 5, 5, 4, 4, 3, 3, 4, 2, 3, 5, 4, 5, 3, 0, 3, 4, 0, 2],[7, 7, 5, 6, 5, 4, 3, 4, 4, 5, 5, 6, 5, 5, 5, 3, 3, 5, 5, 5, 5, 4, 3, 3, 4, 4, 3, 4, 3, 4, 0, 1]])

    for i in range(iteration_count):
        print(i)
        if i < 1:
            dll_tap = optimize_dll_tap(heights_filename, dll_tap,3)
        elif i < 3:
            dll_tap = optimize_dll_tap(heights_filename, dll_tap,2)
        else:
            dll_tap = optimize_dll_tap(heights_filename, dll_tap,1)
        print(dll_tap)
        #if i == 8:
         #   print(f"Re-initializing dll_tap at iteration {i + 1}")
          #  dll_tap = perturbate(dll_tap,3,32)
           # dll_tap = optimize_dll_tap(heights_filename, dll_tap,2)

if __name__ == "__main__":
    main()
