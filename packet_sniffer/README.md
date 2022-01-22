# Packet sniffer

Can be used to sniff packets on an interface of the hacking machine, and to .

## Requirements

* Root access
* Python 2 or 3
* Scapy

## Usage

```shell
usage: packet_sniffer.py [-h] [-i INTERFACE]

Example:
        $ sudo python3 packet_sniffer.py -i eth0
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

Go to sites in browser and view results in terminal where sniffer runs:

```shell
@kali:~$ sudo python3 packet_sniffer.py
[sudo] password for <user>: 
[+] HTTP Request >> testphp.vulnweb.com/userinfo.php

[+] Possible username/password >> b'uname=test&pass=test'

[+] HTTP Request >> sqa.fyicenter.com/1000395_Selenium_Tutorials.html
[+] HTTP Request >> sqa.fyicenter.com/getCommForm.php
[+] HTTP Request >> sqa.fyicenter.com/getCommList.php?ID=1000395&P=0
[+] HTTP Request >> sqa.fyicenter.com/getCommList.php?ID=1000395&P=0
[+] HTTP Request >> sqa.fyicenter.com/Selenium/_icon_Selenium.png
[+] HTTP Request >> sqa.fyicenter.com/SQL-Server-Storage/_icon_SQL-Server-Storage.png
```

## Troubleshooting

* [ImportError on Scapy](https://github.com/tymyrddin/ymrir/wiki/scapy.md)