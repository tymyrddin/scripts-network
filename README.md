# Network scripts

Some python scripting network hacks and network system administration for practising with Python 3 the non-boring way in a familiar domain (or vv).
With many thanks to [EONRaider](https://github.com/EONRaider), [BlackHat](https://www.blackhat.com/), and [ZSecurity](https://zsecurity.org/).

## Requirements

<img align="left" src="https://github.com/tymyrddin/attack-trees/blob/main/assets/images/warning.png">_Do not implement and execute these on a network or system you do not own. Execute only on [your own systems for learning purposes](https://github.com/tymyrddin/ymrir/wiki). Do not execute these on any production network or system, unless "Rules of engagement" have been agreed on, and you have a "Get out of jail free" card of some sort. The scripts have defaults set for our lab. If you wish to run these scripts, change the defaults for your context or provide arguments._

## Scripts

Into the deepest depths of an enterprise target, there are usually no tools to execute network attacks, and no means to install anything.
And in many cases, a Python install can be found ...

### Layer 2

- [x] [MAC changer](layer2/mac_changer)
- [ ] [ARP poisoning](layer2/arp_poisoning)
- [ ] [ARP watcher](layer2/arp_watcher)
- [x] [ARP spoofer](layer2/arp_spoofer)
- [x] [ARP spoof detector](layer2/arp_spoof_detector)

### TCP/IP

- [x] [Client-server skeleton](tcp-ip/client-server)
- [x] [Network scanner](tcp-ip/network_scanner)
- [ ] [TCP proxy](tcp-ip/tcp_proxy)      <= in progress

### DNS

- [x] [DNS spoofer](dns/dns_spoofer)

### HTTP

- [x] [Packet sniffer](http/packet_sniffer)
- [x] [Netcat replace](http/netcat_replace)
- [x] [Code injector](http/code_injector)

### Other

- [x] [File interceptor](other/file_interceptor)
- [x] [Execute system commands](other/execute_commands)
- [x] [Keylogger](other/keylogger)
- [x] [Backdoor](other/backdoor)

## Problems or Suggestions

This project welcomes contributions and suggestions. 

[Open an issue here](https://github.com/tymyrddin/ymrir/issues)