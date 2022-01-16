# DNS Spoofer

## Requirements

* Python 2 or 3
* [NetFilterQueue](https://github.com/oremanj/python-netfilterqueue#installation)
* An iptables `NFQUEUE` (`FORWARD` chain if comes from another device, `OUTPUT` and `INPUT` chain when testing on hacking machine)
* Scapy

```shell
$ sudo iptables -I FORWARD -j NFQUEUE --queue-num 0
```

or

```shell
$ sudo iptables -I OUTPUT -j NFQUEUE --queue-num 0
$ sudo iptables -I INPUT -j NFQUEUE --queue-num 0
```

## Usage

### Example use

Go in the middle:

```shell
$ sudo sysctl -w net.ipv4.ip_forward=1
$ sudo python3 arp_spoofer.py -t 192.168.122.75 -s 192.168.122.1
```

Set up queue and intercept:

```shell
$ sudo iptables -I FORWARD -j NFQUEUE --queue-num 0
$ sudo python3 dns_spoofer.py                      
```

View queue with

```shell
$ sudo cat /proc/net/netfilter/nfnetlink_queue
```

Afterwards, do not forget to disable net.ipv4.ip_forward and to remove the created iptables `NFQUEUE`:

```shell
$ sudo sysctl -w net.ipv4.ip_forward=0
$ sudo iptables --flush
```