#!/usr/bin/env python

import argparse
import os
import subprocess
import time

from mininet.topo import Topo
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.net import Mininet
from mininet.log import lg, info
from mininet.util import dumpNodeConnections
from mininet.cli import CLI
from mininet.clean import cleanup

IPERF3_BASE_PORT = 10000

class FairnessTopo(Topo):
    def build(self, n=2):
        hosts = [
            self.addHost('h1'),
            self.addHost('h2')
        ]
        switch = self.addSwitch('s0')
        delay = str(args.rtt / 4) + 'ms'
        self.addLink(hosts[0], switch, bw=args.bw_host, delay=delay, max_queue_size=args.maxq)
        self.addLink(hosts[1], switch, bw=args.bw_net, delay=delay, max_queue_size=args.maxq)

def start_iperf3_server(net, i, port):
    print(f'Starting iperf3 server {i} on port {port}')
    h2 = net.get('h2')
    h2.popen(f'iperf3 -s -p {port} --forceflush > {args.dir}/iperf3_server_{i}.log 2>&1', shell=True)

def start_iperf3_client(net, cong, i, server_port):
    print(f'Starting iperf3 client {cong}_{i} connecting to port {server_port}')
    h1 = net.get('h1')
    h2 = net.get('h2')
    h1.popen(f'iperf3 -c {h2.IP()} -p {server_port} -w 16m -t {args.time} -C {cong} --forceflush > {args.dir}/iperf3_client_{cong}_{i}.log 2>&1', shell=True)

def main():
    parser = argparse.ArgumentParser(description='BBR Fairness Experiment')

    # Topology configurations
    parser.add_argument('--bw-host', type=float, help='Bandwidth of the host in Mbps', default=1000)
    parser.add_argument('--bw-net', type=float, help='Bandwidth of the bottleneck link in Mbps', default=10)
    parser.add_argument('--rtt', type=float, help='RTT in ms', default=40)
    parser.add_argument('--maxq', type=int, help='Maximum queue size in packets', default=1000)

    # TCP connection configurations
    parser.add_argument('--bbr', type=int, help='Number of BBR connections', default=1)
    parser.add_argument('--reno', type=int, help='Number of Reno connections', default=0)
    parser.add_argument('--cubic', type=int, help='Number of Cubic connections', default=16)

    # Experiment configurations
    parser.add_argument('--dir', type=str, help='Directory to store outputs', default='./outputs')
    parser.add_argument('--time', type=int, help='Duration to run the experiment in seconds', default=300)

    global args
    args = parser.parse_args()

    if not os.path.exists(args.dir):
        os.makedirs(args.dir)

    os.system('sysctl -w net.core.default_qdisc=fq')
    os.system('sysctl -w net.ipv4.tcp_congestion_control=bbr')

    cleanup()

    topo = FairnessTopo()
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
    net.start()

    dumpNodeConnections(net.hosts)
    net.pingAll()

    num_connections = args.bbr + args.reno + args.cubic
    bbr_base_port = IPERF3_BASE_PORT
    reno_base_port = bbr_base_port + args.bbr
    cubic_base_port = reno_base_port + args.reno

    for i in range(num_connections):
        start_iperf3_server(net, i, IPERF3_BASE_PORT + i)
    time.sleep(1)
    for i in range(args.bbr):
        start_iperf3_client(net, 'bbr', i, bbr_base_port + i)
    for i in range(args.reno):
        start_iperf3_client(net, 'reno', i, reno_base_port + i)
    for i in range(args.cubic):
        start_iperf3_client(net, 'cubic', i, cubic_base_port + i)

    start_time = time.time()
    while True:
        now = time.time()
        delta = now - start_time
        if delta >= args.time:
            break
        print(f'Remaining time: {round(args.time - delta)}s        ', end='\r')
        time.sleep(1)
    print('')

    subprocess.Popen(['killall', 'iperf3']).wait()
    net.stop()

if __name__ == '__main__':
    main()
