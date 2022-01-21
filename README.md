# Network scripts

Into the deepest depths of an enterprise target, there are usually no tools to execute network attacks, and no means to install anything.
And in many cases, there is a Python install.

Some python scripting network hacks and network system administration.
With many thanks to Black Hat, Gream and ZSecurity.

## Interfaces
- [x] [Sockets](sockets)
- [x] [MAC changer](mac_changer)

## Using scapy
- [x] [Network scanner](network_scanner)
- [x] [ARP spoofer](arp_spoofer)
- [x] [Packet sniffer](packet_sniffer)
- [x] [DNS spoofer](dns_spoofer)
- [x] [File interceptor](file_interceptor) 
- [x] [Code injector](code_injector)
- [ ] Bypassing HTTPS - in progress
- [ ] ARP spoof detector
- [ ] Netcat replace

## Requirements

* [A small pentesting lab](https://github.com/tymyrddin/ymrir/wiki/pentesting-lab.md) with kali and a windows 10 (virtual) machines. Host was an Ubuntu 20.04. 
* Python 2.7 and Python 3. Most scripts only support Python 3, only a few, for learning purposes, support Python 2.7 (and also Python 3). And [Python 2.7 causes lots of bugs due to end of life](https://github.com/tymyrddin/ymrir/wiki/python-2.7-end-of-life.md).
