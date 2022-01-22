# Network scanner

Scanning for IP address allows for better control over a network. Many existing tools can scan a network, like `netdiscover`, `nmap`, etc. With 1-2 commands, devices (MAC addresses) in a network can be mapped to their IP addresses.

## Requirements

* Root access
* Python 2 or 3
* Scapy module

## Usage

```shell
usage: network_scanner.py [-h] [-t IP]

Network scanner

optional arguments:
  -h, --help      show this help message and exit
  -t IP, --ip IP  IP address range

Example: 
            network_scanner.py -t 192.168.122.1/24 # ip address range
            network_scanner.py -t 192.168.122.1 # ip address
```

## Kicking the tyres

```shell
@kali:~$ sudo python3 network_scanner.py -t 192.168.122.1/24
IP address              MAC Address
-----------------------------------------
192.168.122.1           52:54:00:3a:04:6f
-----------------------------------------
```

## Troubleshooting

* [ImportError on Scapy](https://github.com/tymyrddin/ymrir/wiki/scapy.md)