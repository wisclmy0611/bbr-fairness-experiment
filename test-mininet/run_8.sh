#!/bin/bash
set -e

./setup_env.sh
rm -rf outputs/8*

BBR=(1 2 4 8 16 32)

function run() {
    BW="$1"
    RTT="$2"
    CONG="$3"
    BDPS="$4"
    if [[ "$CONG" = "reno" ]]; then
        TIME=200
        CONG_FLAGS="--reno=1 --cubic=0"
    else
        TIME=400
        CONG_FLAGS="--reno=0 --cubic=1"
    fi
    for bbr in "${BBR[@]}"; do
        for bdp in "${BDPS[@]}"; do
            echo "Running with bandwidth $BW Mbps, RTT ${RTT}ms, queue size $bdp BDP, $bbr BBR flow(s) with 1 $CONG flow for $TIME sec"
            python fairness.py \
                --bw-net=$BW --rtt=$RTT --maxq=$bdp --bbr=$bbr $CONG_FLAGS \
                --dir=./outputs/8/${BW}x$RTT/$CONG/bbr_$bbr/bdp_$bdp --time=$TIME
        done
    done
}

function run_8a() {
    BW=10
    RTT=40
    CONG="cubic"
    BDPS=(1 2 4 8 16 32 64)
    echo "Running 8a"
    run "$BW" "$RTT" "$CONG" "$BDPS"
}

function run_8b() {
    BW=50
    RTT=30
    CONG="cubic"
    BDPS=(1 2 4 8 16)
    echo "Running 8b"
    run "$BW" "$RTT" "$CONG" "$BDPS"
}

function run_8c() {
    BW=10
    RTT=40
    CONG="reno"
    BDPS=(1 2 4 8 16 32 64)
    echo "Running 8c"
    run "$BW" "$RTT" "$CONG" "$BDPS"
}

run_8a && run_8b && run_8c
for f in $(ls outputs/8/*/*/*/*/iperf3_server_*.log); do
    python iperf3_log_parser_bw.py < "$f" > "$f.raw"
done
python plotter_8.py

chown -R mininet:mininet outputs
