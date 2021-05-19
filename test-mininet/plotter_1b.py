#!/usr/bin/env python

import argparse
import matplotlib.pyplot as plt
import re

# Different queue size experiments based on BDP
bdp = [0.25, 0.5, 1, 2, 4, 8, 16, 32, 64, 128]
iteration = range(1, 7)

# Extract average bandwidth from log
REGEX = r'\d+\.\d+-\d+\.\d+ +sec +\d+\.*\d* \w+ +(\d+\.*\d*) (\w+)/sec +receiver'
regex = re.compile(REGEX)

def get_throughputs(experiment, cong, input_dir):
    server_id = 0 if cong == 'bbr' else 1
    sum_throughputs = [0] * len(bdp)
    for cur_iteration in iteration:
        
        throughputs = []
        for cur_bdp in bdp:
            
            filename = f'{input_dir}/{experiment}/iteration_{cur_iteration}/bdp_{cur_bdp}/iperf3_server_{server_id}.log'
            print(f'Reading {filename}')
            with open(filename) as f:
                lines = f.readlines()
                
            result = regex.search(lines[-1])

            bw = float(result[1])
            unit = result[2]

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
