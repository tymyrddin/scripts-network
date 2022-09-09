# ARP spoof detector

The most simple detector.

## Usage

```
usage: arp_spoof_detector.py [-h] [-i INTERFACE]

ARP spoof detector

optional arguments:
  -h, --help            show this help message and exit
  -i INTERFACE, --interface INTERFACE
                        interface to sniff on

Example:
                        arp_spoof_detector.py --i eth0 # sniff on --i interface
                        arp_spoof_detector.py # with default eth0
```

## Kicking the Tyres

* Put in `/etc/init.d/script.py` and make executable `sudo chmod 755 /etc/init.d/scipt.py`
* Register the script to be run at startup with `sudo update-rc.d superscript defaults`