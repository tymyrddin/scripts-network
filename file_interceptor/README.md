# File interceptor

## Requirements

* Root access
* Python 3
* Scapy
* NetfilterQueue

## Usage

```shell
usage: file_interceptor.py [-h] [-e EXTENSION] [-d DESTINATION] [-u URL]

optional arguments:
  -h, --help            show this help message and exit
  -e EXTENSION, --extension EXTENSION
                        Specify a file extension
  -d DESTINATION, --destination DESTINATION
                        Destination (sslstrip, forward, local)
  -u URL, --url URL     Specify a replace url
```

## Troubleshooting

* [ImportError on NetfilterQueue](https://github.com/tymyrddin/ymrir/wiki/netfilterqueue.md)
* [ImportError on Scapy](https://github.com/tymyrddin/ymrir/wiki/scapy.md)