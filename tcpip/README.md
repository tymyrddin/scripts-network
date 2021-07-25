# TCP/IP scripts

These scripts are for educational purposes. If you wish to get serious get tools like [tcpdump](tcpdump.md) and [Wireshark](Wireshark.md).

## Sniffer detection

### Locally

    $ sudo ifconfig -a | grep PROMISC

    $ sudo cat /var/log/messages |grep promisc

### Remotely

* Overflow the network with traffic and continuously ping all connected hosts. In theory a host running a sniffer will respond slower due to more CPU usage for decoding the traffic. A waste of resources and produces false positives.
* Create an ARP packet with a random, unused MAC address other than broadcast (fake broadcast address e.g FF:FF:FF:FF:FF:FE) and target each individual IP on the subnet. Systems that are not running in promiscuous mode will discard it, while sniffing systems will respond. See Scapy function `promiscping()`.

But, it is relatively easy to not be detectable, by using a Lan Tap. It effectively connects the sniffer in parallel to another device but has the Transmit wire disconnected (the monitoring device does not respond to anything).

