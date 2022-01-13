# Network scanner

Many tools can scan network, `netdiscover`, `nmap`, etc. 
This script was made for a better understanding of the ARP protocol, and for some more python programming experience.

## Requirements

* Root access
* Scapy

To install `scapy` for both python 2.7 and python 3, [install for python 3](https://scapy.readthedocs.io/en/latest/installation.html) first, and then copy the `scapy` folder in `dist-packages` to dist-packages of 2.7:

```commandline
- sudo mkdir /usr/lib/python2.7/dist-packages/scapy
- cd /usr/lib/python3/dist-packages/
- cp -avr scapy/* /usr/lib/python2.7/dist-packages/scapy
```