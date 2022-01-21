# Packet sniffer

Can be used to sniff packets on an interface of the hacking machine (possibly after having become MitM with [arp_spoofer](/arp_spoofer)), and to filter for creditials and extracts urls visted.

## Requirements

* Root access
* Python 2 or 3
* Scapy

## Usage

```shell
usage: packet_sniffer.py [-h] [-i INTERFACE]
```

Example:

```shell
$ sudo python3 packet_sniffer.py -i eth0
```

## Troubleshooting

* [ImportError on Scapy](https://github.com/tymyrddin/ymrir/wiki/scapy.md)