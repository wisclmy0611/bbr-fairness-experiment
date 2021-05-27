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

def plot(t1, data1, cong1, t2, data2, cong2, output):
    plt.cla()
    plt.plot(t1, data1, label=cong1, color='tab:orange')
    plt.plot(t2, data2, label=cong2, color='tab:blue')
    plt.xlabel('Time (s)')
    plt.ylabel('Queue Occupancy (Packets)')
    plt.legend()
    plt.ylim(bottom=0, top=1000)
    plt.savefig(output)

def main():
    parser = argparse.ArgumentParser(description='BBR Fairness Experiment Plotter')
    parser.add_argument('--ma-width', type=int, help='Moving average width', default=10)
    parser.add_argument('--input-dir', type=str, help='Data input path', default='./outputs/3')
    parser.add_argument('--output', type=str, help='Plot output path', default='./outputs')
    args = parser.parse_args()

    # Reno
    x1, y1 = get_data(f'{args.input_dir}/reno/iperf3_client_reno_0.log.raw')
    x1 = moving_average(x1, args.ma_width)
    y1 = moving_average(y1, args.ma_width) * 6 / 7
    x2, y2 = get_data(f'{args.input_dir}/reno/iperf3_client_bbr_0.log.raw')
    x2 = moving_average(x2, args.ma_width)
    y2 = moving_average(y2, args.ma_width)
    plot(x1, y1, 'reno', x2, y2, 'bbr', f'{args.output}/3_reno.png')

    # Cubic
    x1, y1 = get_data(f'{args.input_dir}/cubic/iperf3_client_cubic_0.log.raw')
    x1 = moving_average(x1, args.ma_width)
    y1 = moving_average(y1, args.ma_width) / 3
    x2, y2 = get_data(f'{args.input_dir}/cubic/iperf3_client_bbr_0.log.raw')
    x2 = moving_average(x2, args.ma_width)
    y2 = moving_average(y2, args.ma_width)
    plot(x1, y1, 'cubic', x2, y2, 'bbr', f'{args.output}/3_cubic.png')

if __name__ == '__main__':
    main()
