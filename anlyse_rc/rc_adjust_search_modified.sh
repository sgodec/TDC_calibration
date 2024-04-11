#!/bin/bash

max_value_tap1=7
max_value_tap2=7
max_value_tap3=7
max_value_tap4=7

output_file="result.txt"

nan_counter=0
# Define regex patterns for the histograms for each TDC
declare -a tdc1_103_regexes=(".*\/SHIFT\/ToFcalib\/hToFcalib_RC_delay_normC_T3_B2.*" ".*\/SHIFT\/ToFcalib\/hToFcalib_RC_delay_normC_T1_B0.*" ".*\/SHIFT\/ToFcalib\/hToFcalib_RC_delay_normC_T1_B3.*")
declare -a tdc2_103_regexes=(".*\/SHIFT\/ToFcalib\/hToFcalib_RC_delay_normC_T3_B1.*" ".*\/SHIFT\/ToFcalib\/hToFcalib_RC_delay_normC_T1_B2.*")
declare -a tdc3_103_regexes=(".*\/SHIFT\/ToFcalib\/hToFcalib_RC_delay_normC_T3_B0.*" ".*\/SHIFT\/ToFcalib\/hToFcalib_RC_delay_normC_T3_B3.*" ".*\/SHIFT\/ToFcalib\/hToFcalib_RC_delay_normC_T1_B1.*")
declare -a tdc1_104_regexes=(".*\/SHIFT\/ToFcalib\/hToFcalib_RC_delay_normC_T2_B2.*" ".*\/SHIFT\/ToFcalib\/hToFcalib_RC_delay_normC_T0_B0.*" ".*\/SHIFT\/ToFcalib\/hToFcalib_RC_delay_normC_T0_B3.*")
declare -a tdc2_104_regexes=(".*\/SHIFT\/ToFcalib\/hToFcalib_RC_delay_normC_T2_B1.*" ".*\/SHIFT\/ToFcalib\/hToFcalib_RC_delay_normC_T0_B2.*")
declare -a tdc3_104_regexes=(".*\/SHIFT\/ToFcalib\/hToFcalib_RC_delay_normC_T2_B0.*" ".*\/SHIFT\/ToFcalib\/hToFcalib_RC_delay_normC_T2_B3.*" ".*\/SHIFT\/ToFcalib\/hToFcalib_RC_delay_normC_T0_B1.*")
process_tdc_histograms() {
  local tdc_name="$1"
  shift
  local regexes=("$@")
  local heights=""

  for regex in "${regexes[@]}"; do
    # Command to extract histogram data
    is_ls_output=$(is_ls --partition AFP_180 --server Histogramming --regex "$regex" --print-value)
    # Extract the middle values and concatenate them
    middle_values=$(echo "$is_ls_output" | tail -n 1 | awk -F ', ' '{print $2, $3, $4, $5}')
    heights="$heights $middle_values"
  done
  echo "${tdc_name} rc_adjust: $hex_rc_adjust heights:$heights" >> "$output_file"
  if echo "$heights" | grep -q 'nan'; then
    ((nan_counter++))
    if [ "$nan_counter" -ge 3 ]; then
      echo "Three consecutive 'nan' values found. Stopping the process."
      exit 1
    fi
  else
    nan_counter=0
  fi
}
for (( i=0; i<16; i++ )); do
    for (( j=0; j<16; j++ )); do
        for (( k=0; k<16; k++ )); do
            # Construct the 12-bit number
            hex_rc_adjust=$(printf "0x%01X%01X%01X\n" $k $j $i)

            # Apply the configuration
            sed -i "120s/.*/rc_adjust                                  0x$hex_rc_adjust/" /det/afp/configs/moduleconfigs/afp-hptdc/configs/HPTDC103-i2c.cfg
            sed -i "119s/.*/rc_adjust                                  0x$hex_rc_adjust/" /det/afp/configs/moduleconfigs/afp-hptdc/configs/HPTDC104-i2c.cfg

            # Commands for restart and reset
            rc_sender -p AFP_180 -n AFP-RCD-RCE-P1-VLDB -c USER userRCDRestart
            rc_sender -p AFP_180 -n gnamAFP -c USER Reset
            echo "Commands for restart and reset executed, getting data for 30 seconds"
            sleep 1

            # Process histograms for each TDC
            process_tdc_histograms "TDC1_103:" "${tdc1_103_regexes[@]}"
            process_tdc_histograms "TDC2_103:" "${tdc2_103_regexes[@]}"
            process_tdc_histograms "TDC3_103:" "${tdc3_103_regexes[@]}"
            process_tdc_histograms "TDC1_104:" "${tdc1_104_regexes[@]}"
            process_tdc_histograms "TDC2_104:" "${tdc2_104_regexes[@]}"
            process_tdc_histograms "TDC3_104:" "${tdc3_104_regexes[@]}"
            if [ "$nan_counter" -ge 3 ]; then
              exit 1
            fi
        done
    done
  done

echo "All configurations have been processed."

