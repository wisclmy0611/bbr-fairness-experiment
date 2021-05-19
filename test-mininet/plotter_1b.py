#!/usr/bin/env python

import argparse
from os import linesep
import re
import matplotlib.pyplot as plt
import numpy as np


# Different queue size experiments based on BDP
bdp = [0.25, 0.5, 1, 2, 4, 8, 16, 32, 64, 128]
iteration = range(1,2)


# Extract time and bandwidth from log
REGEX = r'(\d+\.\d+)-\d+\.\d+ +sec +\d+\.*\d* \w+ +(\d+\.*\d*) (\w+)/sec'
regex = re.compile(REGEX)


def get_throughputs(experiment, cong, input_dir):
    sum_throughputs = [0 for _ in range(len(bdp))]
    for cur_iteration in iteration:
        
        throughputs = []
        for cur_bdp in bdp:
            
            print (f'Reading {input_dir}/{experiment}/iteration{cur_iteration}/bdp{cur_bdp}/iperf3_client_{cong}_0.log')
            with open(f'{input_dir}/{experiment}/iteration{cur_iteration}/bdp{cur_bdp}/iperf3_client_{cong}_0.log') as f:
                lines = f.readlines()
                
                result = regex.search(lines[-2])
                if result is None:
                    result = regex.search(lines[-4])

                bw = float(result[2])
                unit = result[3]

                if unit == 'Kbits':
                    bw /= 1000
                elif unit == 'bits':
                    bw /= 1000000

                throughputs.append(bw)
        print(throughputs)
        sum_throughputs = [x + y for x, y in zip(sum_throughputs, throughputs)]

    avg_throughput = [x / len(iteration) for x in sum_throughputs]
    print (f'avg {avg_throughput}')
    return avg_throughput

def plot(data1, cong1, data2, cong2, output):
    plt.cla()
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
    cubic_throughputs = get_throughputs('cubic', 'cubic', args.input_dir)
    bbr_throughputs = get_throughputs('cubic', 'bbr', args.input_dir)
    plot(cubic_throughputs, 'cubic', bbr_throughputs, 'bbr', f'{args.output}/1b_cubic.png')

if __name__ == '__main__':
    main()