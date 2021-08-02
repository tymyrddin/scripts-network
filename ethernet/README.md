# Ethernet scripts

Both `arp-cache-poisoning.py` and `mac-flood.py` are merely for increasing understanding and demonstrating how easy these attacks can be.

Both scripts use [scapy](https://scapy.readthedocs.io/en/latest/), which is listed in the requirements.txt, and require disabling the firewall (packet filter) and enabling IP forwarding otherwise host blocks connection with the victim.

    $ sudo sysctl net.ipv4.ip_forward=1

## Tools

Tools that can do what the scripts can do, and more:

* ARP Spoofing: [NetCommander](https://github.com/meh/NetCommander), [Packetstorm ARP attack tool](https://packetstormsecurity.com/files/81368/Hackers-Hideaway-ARP-Attack-Tool.html), [Loki](https://www.c0decafe.de/)
* Sockets: [sockstat](sockstat.md)
* MAC flooding: [Ettercap](https://www.ettercap-project.org/), [Yersinia4](https://kalilinuxtutorials.com/yersinia/), Parasite 6](https://kalilinuxtutorials.com/parasite6/), [macof](https://kalilinuxtutorials.com/macof/), [Loki](https://www.c0decafe.de/)

## Mitigations

### Mac flooding

* Port Security: Limit the number of MAC addresses connecting to a single port on a switch.
* Implement 802.1X: Allows packet filtering rules issued by a centralised AAA server based on dynamic learning of clients.
* MAC Filtering : Limit the number of MAC addresses.
