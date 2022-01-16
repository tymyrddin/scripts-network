# Network scanner

Scanning for IP address allows for better control over a network. Many existing tools can scan a network, like `netdiscover`, `nmap`, etc. With 1-2 commands, devices (MAC addresses) in a network can be mapped to their IP addresses.
 
This script was made for a better understanding of the ARP protocol, and for some more python programming experience.

## Requirements

* Root access
* Python 2 or 3
* Scapy module

## Usage

```shell
usage: network_scanner.py [-h] [-t IP]
```

Example:

```shell
$ sudo python3 network_scanner.py -t 192.168.122.1/24
```
