## Download and install Mininet VM
We need Mininet with the new version 20.04.1 of Ubuntu that has bbr in kernel.
[Image link here](https://github.com/mininet/mininet/releases/download/2.3.0/mininet-2.3.0-210211-ubuntu-20.04.1-legacy-server-amd64-ovf.zip)

## Start Mininet VM and install requirement
```sudo apt install iperf3```

## Start mininet and test iperf3 on h1 h2 host
```
sudo -E mn
xterm h1 h2
```

## For h2 terminal, type:
```
iperf3 -s -i 2
```

## For h1 terminal, type:
```
sysctl -w net.ipv4.tcp_congestion_control=bbr
iperf3 -c 10.0.0.2 -w 16m -t 10 -i 2
```

## Or for h1, just select congestion control algos when typing iperf3 command:
```
iperf3 -c 10.0.0.2 -w 16m -t 10 -i 2 -C bbr
iperf3 -c 10.0.0.2 -w 16m -t 10 -i 2 -C reno
iperf3 -c 10.0.0.2 -w 16m -t 10 -i 2 -C cubic
```

Now we can have h1 host iperf to h2 using bbr and can easily add other hosts that used other congestion algorithms.

## Note for qdisc
For Linux versions before 4.13, pacing support was not part of
the TCP stack but implemented by the Fair Queue (FQ)
queuing discipline.  In BBR source code, they mention setting fq qdisc to avoid using tcp internal pacing that could cause CPU overhead. Here are some references:
- [BBR source code](https://github.com/google/bbr/blob/v2alpha/net/ipv4/tcp_bbr2.c#L56)
- [Qdisc explain](https://www.coverfire.com/articles/queueing-in-the-linux-network-stack/)
- [Discussion of BBR qdisc on google group](https://groups.google.com/g/bbr-dev/c/4jL4ropdOV8)
- [Solid BBR qdisc experimentation](https://kernel.taobao.org/2019/11/bbr-vs-cubic-in-datacenter-network/)
- [fq](https://man7.org/linux/man-pages/man8/tc-fq.8.html)

To set qdisc to fq, we can do:
```
tc qdisc replace dev [interface_name] root fq                       # Add a qdisc to a network interface.
tc -s -d qdisc show dev [interface_name]                            # Show qdisc of a network interface.
```

By default mininet will not set qdisc for the hosts or switches. **Before running iperf3** on h1 host, we should set the qdisc to fq:
```
# Inside h1 terminal
tc qdisc replace dev h1-eth0 root fq
```



## Some questions
Do we have to change other configuration like tcp buffer?
How to measure goodput? Is it the same as the throughput showed by iperf output?
