# DNS Spoofer

## Requirements

* Python 3
* Scapy and netfilter modules
* Domain to be spoofed
* IP address webserver to redirect to

## Usage

```shell
usage: dns_spoofer.py [-h] [-d DOMAIN] [-r IP] [-q DESTINATION]

DNS spoof tool

optional arguments:
  -h, --help            show this help message and exit
  -d DOMAIN, --domain DOMAIN
                        Domain to spoof
  -r IP, --ip IP        IP address to redirect to
  -q DESTINATION, --destination DESTINATION
                        Forward or local

Example: 
            dns_spoofer.py -q forward               # spoof domain on target (Windows)
            dns_spoofer.py -d sqa.fyicenter.com     # domain
            dns_spoofer.py -r 192.168.122.108       # redirection address
            dns_spoofer.py                          # with defaults local, apache2 and sqa.fyicenter.com
```

### Kicking the tyres

Choose a domain to spoof and check it is reachable:

```shell
@kali:~$ ping -c 1 sqa.fyicenter.com
PING sqa.fyicenter.com (74.208.236.35) 56(84) bytes of data.
64 bytes from 74-208-236-35.elastic-ssl.ui-r.com (74.208.236.35): icmp_seq=1 ttl=52 time=131 ms

--- sqa.fyicenter.com ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 131.125/131.125/131.125/0.000 ms

```

Become MitM by running the [arp_spoofer](/layer2/arp_spoofer)

```shell
@kali:~$ sudo python3 arp_spoofer.py
[sudo] password for <user>: 
[+] Setting forward
[+] Packets sent: 63
```

Run DNS spoofer:

```shell
@kali:~$ sudo python3 dns_spoofer.py -q forward
[+] Starting apache2 service...
              
```

On Windows testlab machine, visit http://sqa.fyicenter.com in browser and check that the Kali apache server comes up instead.

```shell
@kali:~$ sudo python3 dns_spoofer.py
[+] Starting apache2 service...
[+] Spoofing Target
                   
```

## Troubleshooting

* [ImportError on NetfilterQueue](https://github.com/tymyrddin/ymrir/wiki/netfilterqueue.md)
* [ImportError on Scapy](https://github.com/tymyrddin/ymrir/wiki/scapy.md)
* [Bettercap sslstrip not working](https://github.com/tymyrddin/ymrir/wiki/bettercap.md)
* [Undesired HTTPS redirects](https://github.com/tymyrddin/ymrir/wiki/https-browser.md)
* [Correctly configured HSTS](https://github.com/tymyrddin/ymrir/wiki/hsts.md)