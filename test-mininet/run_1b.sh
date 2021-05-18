#!/bin/bash
set -e

# rm -rf outputs/*

bw=10
rtt=40
time=240
bdp=(0.25 0.5 1 2 4 8 16 32 64 128)


for bdp in "${bdp[@]}"; do
    for iteration in {1..5}; do
        maxq=$(python -c "print(round($rtt / 1000 * $bw * 1000 * 1000 / 8 / 1500 * $bdp))")
        echo "Running iteration $iteration queue size of $maxq ($bdp bdp)"
        echo "Reno..."
        python fairness.py --bw-host=$bw --bw-net=$bw --rtt=$rtt --maxq=$maxq --bbr=1 --reno=1 --cubic=0 --dir=./outputs/1b/reno/iteration$iteration/bdp$bdp --time=$time
        echo "Cubic..."
        python fairness.py --bw-host=$bw --bw-net=$bw --rtt=$rtt --maxq=$maxq --bbr=1 --reno=0 --cubic=1 --dir=./outputs/1b/cubic/iteration$iteration/bdp$bdp --time=$time
    done
done



# python plotter_1b.py
