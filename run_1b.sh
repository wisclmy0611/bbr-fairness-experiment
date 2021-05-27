#!/bin/bash
set -e

./setup_env.sh
rm -rf outputs/1b*

TIME=240
BDPS=(0.25 0.5 1 2 4 8 16 32 64 128)

for bdp in "${BDPS[@]}"; do
    for iteration in {1..6}; do
        echo "Running iteration $iteration of queue size $bdp BDP"
        echo "Reno..."
        python fairness.py --maxq=$bdp --reno=1 --cubic=0 --dir=./outputs/1b/reno/iteration_$iteration/bdp_$bdp --time=$TIME
        echo "Cubic..."
        python fairness.py --maxq=$bdp --reno=0 --cubic=1 --dir=./outputs/1b/cubic/iteration_$iteration/bdp_$bdp --time=$TIME
    done
done

python plotter_1b.py

chown -R mininet:mininet outputs
