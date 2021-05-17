#!/usr/bin/env python

import argparse
import re
import matplotlib.pyplot as plt
import numpy as np

# Extract time and bandwidth from log
REGEX = r'(\d+\.\d+)-\d+\.\d+ +sec +\d+\.*\d* \w+ +(\d+\.*\d*) (\w+)/sec'
regex = re.compile(REGEX)

# Different queue size experiments based on BDP
bdp = [0.25, 0.5, 1, 2, 4, 8, 16, 32, 64, 128]

def get_throughputs(experiment, cong, input_dir):
    throughputs = []
    for cur_bdp in bdp:
        with open(f'{input_dir}/{experiment}/bdp{cur_bdp}/iperf3_client_{cong}_0.log') as f:
            line = f.readlines()[-2]
            
            result = regex.search(line)
            bw = float(result[2])
            unit = result[3]

            if unit == 'Kbits':
                bw /= 1000
            elif unit == 'bits':
                bw /= 1000000

            throughputs.append(bw)
            print(line)
    print(throughputs)
    return throughputs

def plot(data1, cong1, data2, cong2, output):
    plt.plot(range(len(bdp)), data1, marker='o', label=cong1, color='tab:orange')
    plt.plot(range(len(bdp)), data2, marker='o', label=cong2, color='tab:blue')
    plt.xticks(range(len(bdp)), bdp)
    plt.xlabel('Queue Size (BDP)')
    plt.ylabel('Goodput (Mbps)')
    plt.legend()
    plt.savefig(output)

def main():
    parser = argparse.ArgumentParser(description='BBR Fairness Experiment Plotter')
    parser.add_argument('--input-dir', type=str, help='Data input path', default='./outputs/1b')
    parser.add_argument('--output', type=str, help='Plot output path', default='./outputs')
    args = parser.parse_args()

    # Reno and BBR
    reno_throughputs = get_throughputs('reno', 'reno', args.input_dir)
    bbr_throughputs = get_throughputs('reno', 'bbr', args.input_dir)
    plot(reno_throughputs, 'reno', bbr_throughputs, 'bbr', f'{args.output}/1b_reno.png')

    # Cubic and BBR
    

if __name__ == '__main__':
    main()
