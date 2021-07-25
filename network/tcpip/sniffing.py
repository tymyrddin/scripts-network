"""A simple sniffer script.
Authors: Reinica and Nina

A sniffer sets the NIC of a system to promiscuous mode in order to listen
to all the data transmitted on its segment, and decode the information
encapsulated in the data packets. The data may also be altered in some way
as determined by an attack.

***** Needs to be run with sudo or as superuser *****"""

import socket
import struct
import binascii
import platform


def unpack_ethernet_header(packet):

    ethernet_header = packet[0][0:14]
    ethheader = struct.unpack("!6s6s2s", ethernet_header)

    data = {"Destination MAC:": binascii.hexlify(ethheader[0]),
            " Source MAC:": binascii.hexlify(ethheader[1]),
            " Type:": binascii.hexlify(ethheader[2])}

    return data


def unpack_ip_header(packet):

    ip_header = packet[0][14:34]
    ipheader = struct.unpack("!12s4s4s", ip_header)
    data = {"Source IP:": socket.inet_ntoa(ipheader[1]),
            " Destination IP:": socket.inet_ntoa(ipheader[2])}

    return data


def create_socket():
    # Create a socket with three parameters:
    #   Packet interface: PF_PACKET (Linux) or AF_INET (Windows)
    #   Raw socket
    #   Protocol: 0x0800 (IP)

    operating_system = platform.system()
    if operating_system == "Windows":
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket. htons(0x0800))
    else:  # operating system is Linux
        s = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0800))

    return s


def sniff():
    s = create_socket()

    # Loop forever to get the packets
    while True:
        # Capture packets
        packet = s.recvfrom(2048)
        # Unpack and print packets
        print(unpack_ethernet_header(packet))
        print(unpack_ip_header(packet))


def main():
    sniff()


# Execute
if __name__ == '__main__':
    main()
