#!/bin/bash

# Download the file
scp -J sgodec@lxplus.cern.ch sgodec@pc-tbed-pub:/det/afp/configs/test/result.txt .

# Run the analysis script
python3 anlyser.py 

