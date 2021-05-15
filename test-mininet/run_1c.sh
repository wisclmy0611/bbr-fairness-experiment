#!/bin/bash
set -e

./fairness.py --bw-host=1000 --bw-net=10 --rtt=40 --maxq=1000 --bbr=1 --reno=0 --cubic=16 --dir=./outputs/1c --time=300
for f in $(ls outputs/1c/iperf3_server_*.log); do
    ./iperf3_log_parser.py < "$f" > "$f.raw"
done
./plotter_1c.py --ma-width=100 --input-dir=./outputs/1c --output=./outputs/1c.png
