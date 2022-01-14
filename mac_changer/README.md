# MAC changer

A media access control (MAC) address is a unique identifier assigned to a network interface 
controller by a vendor for use as a network address in communications within a network segment
typically of Ethernet, Wi-Fi, and Bluetooth. 

Changing it can be useful for increasing anonymity, impersonating other devices and bypassing filters.

## Requirements
* Root access
* Python 2 or 3

## Usage

```commandline
usage: mac_changer.py [-h] [-i INTERFACE] [-m NEW_MAC_ADDRESS]
```

Example:

```shell
$ sudo python3 mac_changer.py --i eth0 -m 00:11:11:11:22:55
```




