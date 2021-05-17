#!/bin/bash
set -e

bw=10
rtt=40
time=240
bdp=(0.25 0.5 1 2 4 8 16 32 64 128)

for bdp in "${bdp[@]}"; do
    maxq=$(python -c "print(round($rtt / 1000 * $bw * 1000 * 1000 / 8 / 1500 * $bdp))")
    echo "Running reno experiment with queue size of $maxq ($bdp bdp)"
    python fairness.py --bw-host=$bw --bw-net=$bw --rtt=$rtt --maxq=$maxq --bbr=1 --reno=1 --cubic=0 --dir=./outputs/1b/reno/bdp$bdp --time=$time
done