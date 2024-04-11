#!/bin/bash

output_file="result.txt"

nan_counter=0
# Define regex patterns for the histograms for each TDC
declare -a tdc1_103_regexes=(".*\/SHIFT\/ToFcalib\/RC_norm\/hToFcalib_RC_delay_normC_T3_BC.*" ".*\/SHIFT\/ToFcalib\/RC_norm\/hToFcalib_RC_delay_normC_T1_BA.*" ".*\/SHIFT\/ToFcalib\/RC_norm\/hToFcalib_RC_delay_normC_T1_BD.*")
declare -a tdc2_103_regexes=(".*\/SHIFT\/ToFcalib\/RC_norm\/hToFcalib_RC_delay_normC_T3_BB.*" ".*\/SHIFT\/ToFcalib\/RC_norm\/hToFcalib_RC_delay_normC_T1_BC.*")
declare -a tdc3_103_regexes=(".*\/SHIFT\/ToFcalib\/RC_norm\/hToFcalib_RC_delay_normC_T3_BA.*" ".*\/SHIFT\/ToFcalib\/RC_norm\/hToFcalib_RC_delay_normC_T3_BD.*" ".*\/SHIFT\/ToFcalib\/RC_norm\/hToFcalib_RC_delay_normC_T1_BB.*")
declare -a tdc1_104_regexes=(".*\/SHIFT\/ToFcalib\/RC_norm\/hToFcalib_RC_delay_normC_T2_BC.*" ".*\/SHIFT\/ToFcalib\/RC_norm\/hToFcalib_RC_delay_normC_T0_BA.*" ".*\/SHIFT\/ToFcalib\/RC_norm\/hToFcalib_RC_delay_normC_T0_BD.*")
declare -a tdc2_104_regexes=(".*\/SHIFT\/ToFcalib\/RC_norm\/hToFcalib_RC_delay_normC_T2_BB.*" ".*\/SHIFT\/ToFcalib\/RC_norm\/hToFcalib_RC_delay_normC_T0_BC.*")
declare -a tdc3_104_regexes=(".*\/SHIFT\/ToFcalib\/RC_norm\/hToFcalib_RC_delay_normC_T2_BA.*" ".*\/SHIFT\/ToFcalib\/RC_norm\/hToFcalib_RC_delay_normC_T2_BD.*" ".*\/SHIFT\/ToFcalib\/RC_norm\/hToFcalib_RC_delay_normC_T0_BB.*")
declare -a tdc1_101_regexes=(".*\/SHIFT\/ToFcalib\/RC_norm\/hToFcalib_RC_delay_normA_T3_BC.*" ".*\/SHIFT\/ToFcalib\/RC_norm\/hToFcalib_RC_delay_normA_T1_BA.*" ".*\/SHIFT\/ToFcalib\/RC_norm\/hToFcalib_RC_delay_normA_T1_BD.*")
declare -a tdc2_101_regexes=(".*\/SHIFT\/ToFcalib\/RC_norm\/hToFcalib_RC_delay_normA_T3_BB.*" ".*\/SHIFT\/ToFcalib\/RC_norm\/hToFcalib_RC_delay_normA_T1_BC.*")
declare -a tdc3_101_regexes=(".*\/SHIFT\/ToFcalib\/RC_norm\/hToFcalib_RC_delay_normA_T3_BA.*" ".*\/SHIFT\/ToFcalib\/RC_norm\/hToFcalib_RC_delay_normA_T3_BD.*" ".*\/SHIFT\/ToFcalib\/RC_norm\/hToFcalib_RC_delay_normA_T1_BB.*")
declare -a tdc1_102_regexes=(".*\/SHIFT\/ToFcalib\/RC_norm\/hToFcalib_RC_delay_normA_T2_BC.*" ".*\/SHIFT\/ToFcalib\/RC_norm\/hToFcalib_RC_delay_normA_T0_BA.*" ".*\/SHIFT\/ToFcalib\/RC_norm\/hToFcalib_RC_delay_normA_T0_BD.*")
declare -a tdc2_102_regexes=(".*\/SHIFT\/ToFcalib\/RC_norm\/hToFcalib_RC_delay_normA_T2_BB.*" ".*\/SHIFT\/ToFcalib\/RC_norm\/hToFcalib_RC_delay_normA_T0_BC.*")
declare -a tdc3_102_regexes=(".*\/SHIFT\/ToFcalib\/RC_norm\/hToFcalib_RC_delay_normA_T2_BA.*" ".*\/SHIFT\/ToFcalib\/RC_norm\/hToFcalib_RC_delay_normA_T2_BD.*" ".*\/SHIFT\/ToFcalib\/RC_norm\/hToFcalib_RC_delay_normA_T0_BB.*")

#declare -a tdc1_103_regexes=(".*\/SHIFT\/ToFcalib\/hToFcalib_RC_delay_normC_T3_BC.*" ".*\/SHIFT\/ToFcalib\/hToFcalib_RC_delay_normC_T1_BA.*" ".*\/SHIFT\/ToFcalib\/hToFcalib_RC_delay_normC_T1_BD.*")
#declare -a tdc2_103_regexes=(".*\/SHIFT\/ToFcalib\/hToFcalib_RC_delay_normC_T3_BB.*" ".*\/SHIFT\/ToFcalib\/hToFcalib_RC_delay_normC_T1_BC.*")
#declare -a tdc3_103_regexes=(".*\/SHIFT\/ToFcalib\/hToFcalib_RC_delay_normC_T3_BA.*" ".*\/SHIFT\/ToFcalib\/hToFcalib_RC_delay_normC_T3_BD.*" ".*\/SHIFT\/ToFcalib\/hToFcalib_RC_delay_normC_T1_BB.*")
#declare -a tdc1_104_regexes=(".*\/SHIFT\/ToFcalib\/hToFcalib_RC_delay_normC_T2_BC.*" ".*\/SHIFT\/ToFcalib\/hToFcalib_RC_delay_normC_T0_BA.*" ".*\/SHIFT\/ToFcalib\/hToFcalib_RC_delay_normC_T0_BD.*")
#declare -a tdc2_104_regexes=(".*\/SHIFT\/ToFcalib\/hToFcalib_RC_delay_normC_T2_BB.*" ".*\/SHIFT\/ToFcalib\/hToFcalib_RC_delay_normC_T0_BC.*")
#declare -a tdc3_104_regexes=(".*\/SHIFT\/ToFcalib\/hToFcalib_RC_delay_normC_T2_BA.*" ".*\/SHIFT\/ToFcalib\/hToFcalib_RC_delay_normC_T2_BD.*" ".*\/SHIFT\/ToFcalib\/hToFcalib_RC_delay_normC_T0_BB.*")
#declare -a tdc1_101__regexes=(".*\/SHIFT\/ToFcalib\/hToFcalib_RC_delay_normA_T3_BC.*" ".*\/SHIFT\/ToFcalib\/hToFcalib_RC_delay_normA_T1_BA.*" ".*\/SHIFT\/ToFcalib\/hToFcalib_RC_delay_normA_T1_BD.*")
#declare -a tdc2_101__regexes=(".*\/SHIFT\/ToFcalib\/hToFcalib_RC_delay_normA_T3_BB.*" ".*\/SHIFT\/ToFcalib\/hToFcalib_RC_delay_normA_T1_BC.*")
#declare -a tdc3_101_regexes=(".*\/SHIFT\/ToFcalib\/hToFcalib_RC_delay_normA_T3_BA.*" ".*\/SHIFT\/ToFcalib\/hToFcalib_RC_delay_normA_T3_BD.*" ".*\/SHIFT\/ToFcalib\/hToFcalib_RC_delay_normA_T1_BB.*")
#declare -a tdc1_102_regexes=(".*\/SHIFT\/ToFcalib\/hToFcalib_RC_delay_normA_T2_BC.*" ".*\/SHIFT\/ToFcalib\/hToFcalib_RC_delay_normA_T0_BA.*" ".*\/SHIFT\/ToFcalib\/hToFcalib_RC_delay_normA_T0_BD.*")
#declare -a tdc2_102_regexes=(".*\/SHIFT\/ToFcalib\/hToFcalib_RC_delay_normA_T2_BB.*" ".*\/SHIFT\/ToFcalib\/hToFcalib_RC_delay_normA_T0_BC.*")
#declare -a tdc3_102_regexes=(".*\/SHIFT\/ToFcalib\/hToFcalib_RC_delay_normA_T2_BA.*" ".*\/SHIFT\/ToFcalib\/hToFcalib_RC_delay_normA_T2_BD.*" ".*\/SHIFT\/ToFcalib\/hToFcalib_RC_delay_normA_T0_BB.*")
process_tdc_histograms() {
  local tdc_name="$1"
  shift
  local regexes=("$@")
  local heights=""

  for regex in "${regexes[@]}"; do
    # Command to extract histogram data
    is_ls_output=$(is_ls --partition afpStandaloneVLDB --server Histogramming --regex "$regex" --print-value)
    # Extract the middle values and concatenate them
    middle_values=$(echo "$is_ls_output" | tail -n 1 | awk -F ', ' '{print $2, $3, $4, $5}')
    heights="$heights $middle_values"
  done
  echo "${tdc_name} rc_adjust: $hex_rc_adjust heights:$heights" >> "$output_file"
  if echo "$heights" | grep -q 'nan'; then
    ((nan_counter++))

    if [ "$nan_counter" -ge 120 ]; then

      rc_sender -p afpStandaloneVLDB -n AFP-RCD-RCE-P1-VLDB -c USER reloadConfig
      echo "TTC restart"
	    sleep 30
      rc_sender -p afpStandaloneVLDB -n gnamAFP -c USER Reset
      echo "Commands for restart and reset executed, getting data for 20 seconds"
      sleep 30
    fi
  else
    nan_counter=0
  fi
}
for (( i=0; i<16; i++ )); do
    for (( j=(i == 0 ? 0 : 0); j<16; j++ )); do
        for (( k=((i == 0 && j == 0) ? 0 : 0); k<7; k++ )); do
            # Construct the 12-bit number
            hex_rc_adjust=$(printf "0x%01X%01X%01X\n" $k $j $i)

            # Apply the configuration
            sed -i "122s/.*/rc_adjust                                  $hex_rc_adjust/" /det/afp/configs/moduleconfigs/afp-hptdc/configs/HPTDC103-i2c.cfg
            sed -i "118s/.*/rc_adjust                                  $hex_rc_adjust/" /det/afp/configs/moduleconfigs/afp-hptdc/configs/HPTDC104-i2c.cfg
            sed -i "122s/.*/rc_adjust                                  $hex_rc_adjust/" /det/afp/configs/moduleconfigs/afp-hptdc/configs/HPTDC101-i2c.cfg
            sed -i "117s/.*/rc_adjust                                  $hex_rc_adjust/" /det/afp/configs/moduleconfigs/afp-hptdc/configs/HPTDC102-i2c.cfg

            # Commands for restart and reset
            rc_sender -p afpStandaloneVLDB -n AFP-RCD-RCE-P1-VLDB -c USER reloadConfig
            echo "TTC restart"
            sleep 20
            rc_sender -p afpStandaloneVLDB -n gnamAFP -c USER Reset
            sleep 2
            rc_sender -p afpStandaloneVLDB -n gnamAFP -c USER Reset
            echo "Commands for restart and reset executed, getting data for 30 seconds"
            sleep 32

            # Process histograms for each TDC
            process_tdc_histograms "TDC1_103:" "${tdc1_103_regexes[@]}"
            process_tdc_histograms "TDC2_103:" "${tdc2_103_regexes[@]}"
            process_tdc_histograms "TDC3_103:" "${tdc3_103_regexes[@]}"
            process_tdc_histograms "TDC1_104:" "${tdc1_104_regexes[@]}"
            process_tdc_histograms "TDC2_104:" "${tdc2_104_regexes[@]}"
            process_tdc_histograms "TDC3_104:" "${tdc3_104_regexes[@]}"
            process_tdc_histograms "TDC1_101:" "${tdc1_101_regexes[@]}"
            process_tdc_histograms "TDC2_101:" "${tdc2_101_regexes[@]}"
            process_tdc_histograms "TDC3_101:" "${tdc3_101_regexes[@]}"
            process_tdc_histograms "TDC1_102:" "${tdc1_102_regexes[@]}"
            process_tdc_histograms "TDC2_102:" "${tdc2_102_regexes[@]}"
            process_tdc_histograms "TDC3_102:" "${tdc3_102_regexes[@]}"
        done
      	k = 0
    done
    j = 0
  done
  i = 0

echo "All configurations have been processed."



