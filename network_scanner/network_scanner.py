#!/usr/bin/env python3

import argparse             # https://docs.python.org/3/library/argparse.html
import os                   # https://docs.python.org/3/library/os.html
import scapy.all as scapy   # https://scapy.readthedocs.io/en/latest/index.html
import sys                  # https://docs.python.org/3/library/sys.html
import textwrap             # https://docs.python.org/3/library/textwrap.html


def is_not_root():
    return os.geteuid() != 0


def get_args():
    parser = argparse.ArgumentParser(
        description="Network scanner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """Example: 
            network_scanner.py -t 192.168.122.1/24 # ip address range
            network_scanner.py -t 192.168.122.1 # ip address
        """
        ),
    )
    parser.add_argument("-t", "--ip", default="192.168.122.1/24", help="IP address range")
    values = parser.parse_args()
    return values


def scan(ip):
    # Create ARP broadcast request
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    # Send and receive
    answers = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    # Parse responses
    clients = []
    for answer in answers:
        client = {"ip": answer[1].psrc, "mac": answer[1].hwsrc}
        clients.append(client)
    return clients


def print_results(results):
    print("IP address\t\tMAC Address")
    print("-----------------------------------------")
    for result in results:
        print(result["ip"] + "\t\t" + result["mac"])
    print("-----------------------------------------")


if __name__ == "__main__":
    if is_not_root():
        sys.exit("[-] This script requires superuser privileges.")

options = get_args()
scan_results = scan(options.ip)
print_results(scan_results)
