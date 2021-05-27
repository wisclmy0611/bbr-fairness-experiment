#!/usr/bin/env python

import argparse

import matplotlib.pyplot as plt
import numpy as np

# https://stackoverflow.com/questions/14313510/how-to-calculate-rolling-moving-average-using-numpy-scipy
def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w

def get_data(filename):
    with open(filename) as f:
        lines = f.readlines()
    x = []
    y = []
    for line in lines:
        line = line.split()
        x.append(float(line[0]))
        y.append(float(line[1]))
    return x, y

def main():
    parser = argparse.ArgumentParser(description='BBR Fairness Experiment Plotter')
    parser.add_argument('--ma-width', type=int, help='Moving average width', default=20)
    parser.add_argument('--input-dir', type=str, help='Data input path', default='./outputs/1c')
    parser.add_argument('--output', type=str, help='Plot output path', default='./outputs/1c.png')
    args = parser.parse_args()

    # BBR
    x1, y1 = get_data(f'{args.input_dir}/iperf3_server_0.log.raw')
    x1 = moving_average(x1, args.ma_width)
    y1 = moving_average(y1, args.ma_width)
    plt.plot(x1, y1, label='1 BBR flow', color='tab:blue')

    # Cubics
    x2 = []
    y2 = []
    for i in range(1, 17):
        t1, t2 = get_data(f'{args.input_dir}/iperf3_server_{i}.log.raw')
        x2.append(t1)
        y2.append(t2)
    x2 = max(x2, key=lambda x: len(x))
    l = len(x2)
    for y in y2:
        y.extend([0] * (l - len(y)))
    y2 = np.array(y2).sum(axis=0)
    x2 = moving_average(x2, args.ma_width)
    y2 = moving_average(y2, args.ma_width)
    plt.plot(x2, y2, label='Sum of 16 Cubic flows', color='tab:orange')

    plt.xlabel('Time (s)')
    plt.ylabel('Goodput (Mbps)')
    plt.legend()

    plt.savefig(args.output)

if __name__ == '__main__':
    main()
