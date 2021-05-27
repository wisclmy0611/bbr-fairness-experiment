# BBR Fairness Experiment

This project aims to reproduce the results from the paper [*Modeling BBR's Interactions with Loss-Based Congestion Control*](https://dl.acm.org/doi/10.1145/3355369.3355604), which tries to investigate and model the fraction of bandwidth BBR flows take when competing with traditional loss-based congestion control algorithms, such as Reno and Cubic. We're trying to reproduce figure 1b, 1c, 3, and 8 from the original paper. Results can be found in the [`results`](results) directory.

## Instructions

To run the experiments and reproduce the results, you'll need to:

1. Download and install Mininet VM  
    We need [Mininet VM with Ubuntu 20.04](https://github.com/mininet/mininet/releases/download/2.3.0/mininet-2.3.0-210211-ubuntu-20.04.1-legacy-server-amd64-ovf.zip) that has BBR in the kernel.
2. Start the VM
3. Install dependencies
    ```
    sudo apt install iperf3
    sudo pip3 install matplotlib
    ```
4. Clone this repo
    ```
    git clone https://github.com/wisclmy0611/bbr-fairness-experiment
    cd bbr-fairness-experiment
    ```
5. Run all the experiments
    ```
    sudo ./run.sh
    ```
    or if you want to run individual experiments
    ```
    sudo ./run_1b.sh
    sudo ./run_1c.sh
    sudo ./run_3_cwnd.sh
    sudo ./run_8.sh
    ```
    The experiments in total take about 18 hours to run.
