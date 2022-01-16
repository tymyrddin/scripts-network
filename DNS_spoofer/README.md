# DNS Spoofer

## Requirements

* Scapy
* [NetFilterQueue](https://github.com/oremanj/python-netfilterqueue#installation)
* Setting up an iptables "nfqueue"

```shell
$ sudo iptables -I FORWARD -j NFQUEUE --queue-num 0
```

## Usage


View queue with

```shell
$ sudo cat /proc/net/netfilter/nfnetlink_queue
```