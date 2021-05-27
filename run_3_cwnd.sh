#!/bin/bash
set -e

./setup_env.sh
rm -rf outputs/3*

RTT=20
TIME=240
BDP=64

python fairness.py --dir=./outputs/3/reno --rtt=$RTT --maxq=$BDP --reno=1 --cubic=0 --time=$TIME
python fairness.py --dir=./outputs/3/cubic --rtt=$RTT --maxq=$BDP --reno=0 --cubic=1 --time=$TIME
for f in $(ls outputs/3/*/iperf3_client_*.log); do
    python iperf3_log_parser_cwnd.py < "$f" > "$f.raw"
done
python plotter_3_cwnd.py

chown -R mininet:mininet outputs
