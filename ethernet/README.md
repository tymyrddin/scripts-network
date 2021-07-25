# Ethernet scripts

Both `arp-cache-poisoning.py` and `mac-flood.py` are merely for increasing understanding and demonstrating how easy these attacks can be.

Both scripts use [scapy](https://scapy.readthedocs.io/en/latest/), which is listed in the requirements.txt, and require disabling the firewall (packet filter) and enabling IP forwarding otherwise host blocks connection with the victim.

    $ sudo sysctl net.ipv4.ip_forward=1

## Tools

Tools that can do what the scripts can do, and that are further evolved (can do more)

* [NetCommander](https://github.com/meh/NetCommander)
* [Packetstorm ARP attack tool](https://packetstormsecurity.com/files/81368/Hackers-Hideaway-ARP-Attack-Tool.html)
* [Loki](https://www.c0decafe.de/)
* [sockstat](sockstat.md)