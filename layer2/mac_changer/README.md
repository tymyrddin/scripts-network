# MAC changer

A media access control (MAC) address is a unique identifier assigned to a network interface 
controller by a vendor for use as a network address in communications within a network segment
typically of Ethernet, Wi-Fi, and Bluetooth. 

Changing it can be useful for increasing anonymity, impersonating other devices and bypassing filters.

## Requirements
* Root access
* Python 2 or 3

## Usage

```shell
usage: mac_changer.py [-h] [-i INTERFACE] [-m MAC]

MAC address changer tool

optional arguments:
  -h, --help            show this help message and exit
  -i INTERFACE, --interface INTERFACE
                        interface to change MAC address for
  -m MAC, --mac MAC     new MAC address

Example: 
            mac_changer.py --i eth0 -m 00:11:11:11:22:55
```

## Kicking the tyres

Check current MAC address of Kali machine with `ifconfig` (the ether address is the MAC address):

```shell
@kali:~$ ifconfig
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.122.108  netmask 255.255.255.0  broadcast 192.168.122.255
        inet6 fe80::5054:ff:fe99:3df3  prefixlen 64  scopeid 0x20<link>
        ether 52:54:00:99:3d:f3  txqueuelen 1000  (Ethernet)
        RX packets 27332  bytes 22938656 (21.8 MiB)
        RX errors 0  dropped 1870  overruns 0  frame 0
        TX packets 19579  bytes 2228743 (2.1 MiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 4150  bytes 500598 (488.8 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 4150  bytes 500598 (488.8 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```

Maybe use the [MAC validator](http://sqa.fyicenter.com/1000208_MAC_Address_Validator.html) 

```shell
Specified MAC Address: Valid ✔

MAC address specified: 00:11:11:11:22:55
MAC address normalized: 00-11-11-11-22-55

Is It Unicast or Multicast?
   Unicast: First bit = 0. Identifies a single device.

Is It Global or Local?
   Global: Second bit = 0. Valid globally.

Manufacturer Info: 
   OUI: 00-11-11
   Name: Intel Corporation
   Address: 
      2111 NE 25th Avenue
      Hillsboro  OR  97124
      US
```

Run the script:

```shell
@kali:~$ sudo python3 mac_changer.py --i eth0 -m 00:11:11:11:22:55
[sudo] password for <user>: 
[+] Current MAC address: 52:54:00:99:3d:f3
[+] Changing MAC address for eth0 to 00:11:11:11:22:55
[+] MAC address has changed to 00:11:11:11:22:55
```

Check with `ifconfig` that the MAC address has changed.

