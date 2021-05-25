#!/usr/bin/env python

import argparse
import matplotlib.pyplot as plt
import numpy as np

BBR = [1, 2, 4, 8, 16, 32]

def bdp_to_maxq(bdp, bw, rtt):
    return round(bdp * bw * rtt / 12)

def model_raw(N, q, c, l, X, d):
    p = 1 / 2 - 1 / (2 * X) - 4 * N / q
    probe_time = (q / c + 0.2 + l) * d / 10
    bbr_frac = (1 - p) * (d - probe_time) / d
    return bbr_frac

def model(bw, rtt, time, bbr, bdp):
    N = bbr
    q = bdp_to_maxq(bdp, bw, rtt)
    c = bw * 250 / 3
    l = rtt / 1000
    X = bdp
    d = time
    ret = model_raw(N, q, c, l, X, d)
    return 1 if ret > 1 else ret

def get_data_single(bw, bbr, input_dir):
    data = []
    for i in range(bbr):
        with open(f'{input_dir}/iperf3_server_{i}.log.raw') as f:
            lines = f.readlines()
        data.append([float(line.split()[1]) for line in lines])
    max_l = max(len(y) for y in data)
    for y in data:
        y.extend([0] * (max_l - len(y)))
    data = np.array(data).sum(axis=0)
    data = np.average(data[-args.avg_width:])
    return data / bw

def get_data(bw, bbr, bdps, input_dir):
    return [get_data_single(bw, bbr, f'{input_dir}/bdp_{bdp}') for bdp in bdps]

def plot_subfigure(bw, rtt, time, bbr, bdps, input_dir, output):
    actual = get_data(bw, bbr, bdps, input_dir)
    model_output = [model(bw, rtt, time, bbr, bdp) for bdp in bdps]
    plt.cla()
    plt.plot(range(len(bdps)), actual, marker='o', label='Actual', color='tab:blue')
    plt.plot(range(len(bdps)), model_output, marker='o', label='Model', color='tab:orange')
    plt.xticks(range(len(bdps)), bdps)
    plt.xlabel('Queue Size (BDP)')
    plt.ylabel('BBR Flows Aggregate Link Fraction')
    plt.legend()
    plt.savefig(output)

def plot(bw, rtt, cong, bdps, input_dir, output_prefix):
    time = 200 if cong == 'reno' else 400
    for bbr in BBR:
        plot_subfigure(bw, rtt, time, bbr, bdps, f'{input_dir}/bbr_{bbr}', f'{output_prefix}_bbr_{bbr}.png')

def plot_8a():
    bw = 10
    rtt = 40
    cong = 'cubic'
    bdps = [1, 2, 4, 8, 16, 32, 64]
    plot(bw, rtt, cong, bdps, f'{args.input_dir}/{bw}x{rtt}/{cong}', f'{args.output}/8a')

def plot_8b():
    bw = 50
    rtt = 30
    cong = 'cubic'
    bdps = [1, 2, 4, 8, 16]
    plot(bw, rtt, cong, bdps, f'{args.input_dir}/{bw}x{rtt}/{cong}', f'{args.output}/8b')

def plot_8c():
    bw = 10
    rtt = 40
    cong = 'reno'
    bdps = [1, 2, 4, 8, 16, 32, 64]
    plot(bw, rtt, cong, bdps, f'{args.input_dir}/{bw}x{rtt}/{cong}', f'{args.output}/8c')

def main():
    parser = argparse.ArgumentParser(description='BBR Fairness Experiment Plotter')
    parser.add_argument('--avg-width', type=int, help='Average width', default=200)
    parser.add_argument('--input-dir', type=str, help='Data input path', default='./outputs/8')
    parser.add_argument('--output', type=str, help='Plot output path', default='./outputs')
    global args
    args = parser.parse_args()

    plot_8a()
    plot_8b()
    plot_8c()

if __name__ == '__main__':
    main()
