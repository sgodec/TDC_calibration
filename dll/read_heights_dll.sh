#!/bin/bash

output_file="heights.txt"
> "$output_file"
# Define regex patterns for the histograms for each TDC

declare -a tdc1_103_regexes=(".*\/SHIFT\/ToFcalib\/DLL_norm\/hToFcalib_DLL_tap_normC_T3_BC.*" ".*\/SHIFT\/ToFcalib\/DLL_norm\/hToFcalib_DLL_tap_normC_T1_BA.*" ".*\/SHIFT\/ToFcalib\/DLL_norm\/hToFcalib_DLL_tap_normC_T1_BD.*")
declare -a tdc2_103_regexes=(".*\/SHIFT\/ToFcalib\/DLL_norm\/hToFcalib_DLL_tap_normC_T3_BB.*" ".*\/SHIFT\/ToFcalib\/DLL_norm\/hToFcalib_DLL_tap_normC_T1_BC.*")
declare -a tdc3_103_regexes=(".*\/SHIFT\/ToFcalib\/DLL_norm\/hToFcalib_DLL_tap_normC_T3_BA.*" ".*\/SHIFT\/ToFcalib\/DLL_norm\/hToFcalib_DLL_tap_normC_T3_BD.*" ".*\/SHIFT\/ToFcalib\/DLL_norm\/hToFcalib_DLL_tap_normC_T1_BB.*")
declare -a tdc1_104_regexes=(".*\/SHIFT\/ToFcalib\/DLL_norm\/hToFcalib_DLL_tap_normC_T2_BC.*" ".*\/SHIFT\/ToFcalib\/DLL_norm\/hToFcalib_DLL_tap_normC_T0_BA.*" ".*\/SHIFT\/ToFcalib\/DLL_norm\/hToFcalib_DLL_tap_normC_T0_BD.*")
declare -a tdc2_104_regexes=(".*\/SHIFT\/ToFcalib\/DLL_norm\/hToFcalib_DLL_tap_normC_T2_BB.*" ".*\/SHIFT\/ToFcalib\/DLL_norm\/hToFcalib_DLL_tap_normC_T0_BC.*")
declare -a tdc3_104_regexes=(".*\/SHIFT\/ToFcalib\/DLL_norm\/hToFcalib_DLL_tap_normC_T2_BA.*" ".*\/SHIFT\/ToFcalib\/DLL_norm\/hToFcalib_DLL_tap_normC_T2_BD.*" ".*\/SHIFT\/ToFcalib\/DLL_norm\/hToFcalib_DLL_tap_normC_T0_BB.*")
declare -a tdc1_101_regexes=(".*\/SHIFT\/ToFcalib\/DLL_norm\/hToFcalib_DLL_tap_normA_T3_BC.*" ".*\/SHIFT\/ToFcalib\/DLL_norm\/hToFcalib_DLL_tap_normA_T1_BA.*" ".*\/SHIFT\/ToFcalib\/DLL_norm\/hToFcalib_DLL_tap_normA_T1_BD.*")
declare -a tdc2_101_regexes=(".*\/SHIFT\/ToFcalib\/DLL_norm\/hToFcalib_DLL_tap_normA_T3_BB.*" ".*\/SHIFT\/ToFcalib\/DLL_norm\/hToFcalib_DLL_tap_normA_T1_BC.*")
declare -a tdc3_101_regexes=(".*\/SHIFT\/ToFcalib\/DLL_norm\/hToFcalib_DLL_tap_normA_T3_BA.*" ".*\/SHIFT\/ToFcalib\/DLL_norm\/hToFcalib_DLL_tap_normA_T3_BD.*" ".*\/SHIFT\/ToFcalib\/DLL_norm\/hToFcalib_DLL_tap_normA_T1_BB.*")
declare -a tdc1_102_regexes=(".*\/SHIFT\/ToFcalib\/DLL_norm\/hToFcalib_DLL_tap_normA_T2_BC.*" ".*\/SHIFT\/ToFcalib\/DLL_norm\/hToFcalib_DLL_tap_normA_T0_BA.*" ".*\/SHIFT\/ToFcalib\/DLL_norm\/hToFcalib_DLL_tap_normA_T0_BD.*")
declare -a tdc2_102_regexes=(".*\/SHIFT\/ToFcalib\/DLL_norm\/hToFcalib_DLL_tap_normA_T2_BB.*" ".*\/SHIFT\/ToFcalib\/DLL_norm\/hToFcalib_DLL_tap_normA_T0_BC.*")
declare -a tdc3_102_regexes=(".*\/SHIFT\/ToFcalib\/DLL_norm\/hToFcalib_DLL_tap_normA_T2_BA.*" ".*\/SHIFT\/ToFcalib\/DLL_norm\/hToFcalib_DLL_tap_normA_T2_BD.*" ".*\/SHIFT\/ToFcalib\/DLL_norm\/hToFcalib_DLL_tap_normA_T0_BB.*")

# Declare arrays for each TDC's regex patterns
declare -a tdc_regex_arrays=(tdc1_103_regexes tdc2_103_regexes tdc3_103_regexes tdc1_104_regexes tdc2_104_regexes tdc3_104_regexes tdc1_101_regexes tdc2_101_regexes tdc3_101_regexes tdc1_102_regexes tdc2_102_regexes tdc3_102_regexes)



process_tdc_histograms() {
    local regexes=("$@") # All arguments are regex patterns
    local heights=""

    for regex in "${regexes[@]}"; do
        local is_ls_output=$(is_ls -p afpStandaloneVLDB --server Histogramming --regex "$regex" --print-value)
        local middle_values=$(echo "$is_ls_output" | tail -n 1 | awk -F ', ' '{for (i=2; i<=33; i++) printf "%s ", $i; print ""}')
        heights="$heights$middle_values"
    done

    echo "$heights"
}

for tdc_regex_array_name in "${tdc_regex_arrays[@]}"; do
            declare -n tdc_regexes="$tdc_regex_array_name"
            process_tdc_histograms "${tdc_regexes[@]}" >>"$output_file"
done
