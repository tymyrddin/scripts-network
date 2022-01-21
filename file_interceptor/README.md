# File interceptor

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

```shell
ImportError: No module named netfilterqueue
```

```shell
sudo apt-get install python3-pip git apache2 tcpdump libnfnetlink-dev libnetfilter-queue-dev
sudo pip3 install --upgrade -U git+https://github.com/kti/python-netfilterqueue
```