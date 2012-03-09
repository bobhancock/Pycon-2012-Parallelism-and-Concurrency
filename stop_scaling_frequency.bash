#! /bin/bash

# Some PCs will scale down CPU performance to save power.
# This should disable it.

for i in /sys/devices/system/cpu/cpu[0-9]
do
    echo performance > $i/cpufreq/scaling_governor
done