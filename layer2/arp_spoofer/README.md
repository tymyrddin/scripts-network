# ARP Spoofer

ARP spoofing, ARP cache poisoning, or ARP poison routing, is a technique by which an attacker sends an ARP request to a device on a local area network, associating its MAC address with the IP addresses of other devices. 
Most likely this includes the default router or gateway, causing any traffic from the local network meant for it to be sent to the attacker instead.

There are many existing tools like [arpspoof](https://github.com/tymyrddin/nest-egg/blob/main/cheatsheets/ARP-spoof-cheat.md) that can do this. And programming such an ARP Spoofer is excellent practice.

## Requirements

* Root access
* Python 3
* Scapy

## Usage

```shell
usage: arp_spoofer.py [-h] [-t TARGET] [-r ROUTER]

ARP spoof tool

optional arguments:
  -h, --help            show this help message and exit
  -t TARGET, --target TARGET
                        target IP address
  -r ROUTER, --router ROUTER
                        spoof this IP address

Example: 
            arp_spoofer.py -t 192.168.122.75 -s 192.168.122.1
            arp_spoofer.py  # with defaults -t 192.168.122.75 -s 192.168.122.1                                                                      
```

## Troubleshooting

* [ImportError on Scapy](https://github.com/tymyrddin/ymrir/wiki/scapy.md)