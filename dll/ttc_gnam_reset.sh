#!/bin/bash


rc_sender -p afpStandaloneVLDB -n AFP-RCD-RCE-P1-VLDB -c USER reloadConfig
echo "TTC restart"
sleep 10
rc_sender -p afpStandaloneVLDB -n gnamAFP -c USER Reset
sleep 5
rc_sender -p afpStandaloneVLDB -n gnamAFP -c USER Reset
echo "Commands for restart and reset executed, getting data for 100 seconds"
sleep 100

