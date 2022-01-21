# Network scripts

Into the deepest depths of an enterprise target, there are usually no tools to execute network attacks, and no means to install anything.
And in many cases, there is a Python install.

Some python scripting network hacks and network system administration.
With many thanks to Black Hat, Gream and ZSecurity.

## Interfaces
- [x] [Sockets](sockets)
- [x] [MAC changer](mac_changer)

## Using scapy
- [x] [Network scanner](network_scanner)
- [x] [ARP spoofer](arp_spoofer)
- [x] [Packet sniffer](packet_sniffer)
- [x] [DNS spoofer](dns_spoofer)
- [x] [File interceptor](file_interceptor) 
- [x] [Code injector](code_injector)
- [ ] Bypassing HTTPS - in progress
- [ ] ARP spoof detector
- [ ] Netcat replace

## Requirements

* A small pentesting lab with kali and a windows 10 (virtual) machines. Host was an Ubuntu 20.04. 
* Python 2.7 and Python 3. Most scripts only support Python 3, only a few, for learning purposes, support Python 2.7 (and also Python 3).

### Testlab

If the machine you are on supports virtualization, on Ubuntu you can use VMWare and ready-made guests or use KVM and make the virtual machines yourself.
Do not run both virtualizations, or turn off one in `systemctl` when using the other. It's a hassle though.

If you do not have virtualization, you can set up a lab with a few old buckets.

In all cases you can use testing versions from Microsoft (for 90 days). In virtualized machines make a snapshot immediately after install, to return to when time runs out.

#### Use VMWare 
* [Microsoft test VM's](https://developer.microsoft.com/en-us/microsoft-edge/tools/vms/) - 90 days
* [ZSecurity kali linux VM](https://zsecurity.org/download-custom-kali/) - set it to 4G RAM

#### Use KVM
* [Windows 10 enterprise edition iso](https://www.microsoft.com/en-us/evalcenter/evaluate-windows-10-enterprise) - 90 days
* [Windows 10 Home or Pro iso](https://www.microsoft.com/en-in/software-download/windows10ISO) - Though you can download the image for free, you will have to use your own license key later.
* [How To Install Windows 10 on Ubuntu KVM?](https://getlabsdone.com/install-windows-10-on-ubuntu-kvm/)
* [Hosting a Kali Linux virtual machine using KVM on an Ubuntu 20.10 box](https://heds.nz/posts/hosting-kali-linux-kvm-ubuntu/)
* [Running Windows 10 on Linux using KVM with VGA Passthrough](https://www.heiko-sieger.info/running-windows-10-on-linux-using-kvm-with-vga-passthrough/)

### Python 2.7 and Python 3

```shell
Python 2.7 will reach the end of its life on January 1st, 2020. Please upgrade your Python as Python 2.7 won’t be maintained after that date. A future version of pip will drop support for Python 2.7.
```

Python 2.7 causes lots of bugs due to end of life. But many scripts in kali (and elsewhere) are still in 2.7.

Common errors:

```shell
kali:~$ ImportError: No module named <Package Name>
kali:~$ pip: command not found error
```