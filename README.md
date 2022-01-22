# Network scripts

Some python scripting network hacks and network system administration for learning python the non-boring way in a familiar domain (or vv).
With many thanks to [EONRaider](https://github.com/EONRaider), [BlackHat](https://www.blackhat.com/), and [ZSecurity](https://zsecurity.org/).

## Requirements
* [A small pentesting lab](https://github.com/tymyrddin/ymrir/wiki/pentesting-lab.md) with Kali and a Windows 10 (virtual) machines. Host was an Ubuntu 20.04. 
* Most scripts only support Python 3, only a few, for learning purposes, support Python 2.7 (and also Python 3). And [Python 2.7 causes lots of bugs due to end of life](https://github.com/tymyrddin/ymrir/wiki/python-2.7-end-of-life.md).

## Getting started

The basics of ethical hacking and Python programming at the same time.

- [x] [MAC changer](mac_changer) - module re, system commands, variables, strings, input, argument parsing, functions, conditional statements.
- [x] [Network scanner](network_scanner) - scapy, combining frames, lists, escaping characters, dictionaries, iterating over nested data structures.
- [x] [ARP spoofer](arp_spoofer) - scapy module, loops and counters, dynamic printing, exception handling
- [x] [Packet sniffer](packet_sniffer) - scapy module, time module, extracting data from a specific layer, strings and bytes (in python 3)
- [x] [DNS spoofer](dns_spoofer) - scapy module, creating a proxy, converting, filtering, analysing and modifying packets
- [x] [File interceptor](file_interceptor) - scapy module, filtering, analysing, intercepting, and modifying http requests, replacing downloads on the network
- [x] [Code injector](code_injector) - regex, groups and None-capturing regex, decoding http responses, injecting JS code, recalculating content length, integrating BeEF
- [ ] [Bypassing HTTPS](bypass_https) - sniffing login credentials, replacing downloads on https pages, injecting code in https pages
- [ ] ARP spoof detector - python on Windows, capturing and analysing ARP responses, detecting ARP spoofing

## Getting useful

Into the deepest depths of an enterprise target, there are usually no tools to execute network attacks, and no means to install anything.
And in many cases, a Python install can be found.

- [x] [Sockets](sockets) - PEP script structures
- [x] [Netcat replace](netcat_replace) - classes
- [ ] TCP proxy - in progress
- [ ] SSH tunneling
- [ ] Decoding the IP Layer

