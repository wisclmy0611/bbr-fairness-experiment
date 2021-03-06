#!/bin/bash
set -e

./setup_env.sh
rm -rf outputs/1c*

python fairness.py --dir=./outputs/1c --delay-bbr-others=0.5
for f in $(ls outputs/1c/iperf3_server_*.log); do
    python iperf3_log_parser_bw.py < "$f" > "$f.raw"
done
python plotter_1c.py

chown -R mininet:mininet outputs
