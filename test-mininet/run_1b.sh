#!/bin/bash
set -e

# make sure we don't use a cached cwnd
sysctl -w net.ipv4.tcp_no_metrics_save=1
# make sure the local socket buffers don't become the bottleneck
sysctl -w "net.ipv4.tcp_mem=10240 87380 268435456"

rm -rf outputs/*

bw=10
rtt=40
time=240
bdp=(0.25 0.5 1 2 4 8 16 32 64 128)

for bdp in "${bdp[@]}"; do
    for iteration in {1..1}; do
        maxq=$(python -c "print(round($rtt / 1000 * $bw * 1000 * 1000 / 8 / 1500 * $bdp))")
        echo "Running iteration $iteration queue size of $maxq ($bdp bdp)"
        echo "Reno..."
        python fairness.py --bw-host=1000 --bw-net=$bw --rtt=$rtt --maxq=$maxq --bbr=1 --reno=1 --cubic=0 --dir=./outputs/1b/reno/iteration$iteration/bdp$bdp --time=$time
        echo "Cubic..."
        python fairness.py --bw-host=1000 --bw-net=$bw --rtt=$rtt --maxq=$maxq --bbr=1 --reno=0 --cubic=1 --dir=./outputs/1b/cubic/iteration$iteration/bdp$bdp --time=$time
    done
done



python plotter_1b.py
