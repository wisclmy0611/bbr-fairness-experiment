#!/bin/bash
set -e

# Enable bbr
sysctl -w net.core.default_qdisc=fq
sysctl -w net.ipv4.tcp_congestion_control=bbr

# make sure we don't use a cached cwnd
sysctl -w net.ipv4.tcp_no_metrics_save=1
# make sure the local socket buffers don't become the bottleneck
sysctl -w "net.ipv4.tcp_mem=10240 87380 268435456"
