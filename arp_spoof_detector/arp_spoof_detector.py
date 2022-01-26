#!/usr/bin/env python3

import argparse  # https://docs.python.org/3/library/argparse.html
import scapy.all as scapy  # https://scapy.readthedocs.io/en/latest/index.html
import textwrap  # https://docs.python.org/3/library/textwrap.html


def get_args():
	parser = argparse.ArgumentParser(
		description="ARP spoof detector",
		formatter_class=argparse.RawDescriptionHelpFormatter,
		epilog=textwrap.dedent(
			"""Example: 
			arp_spoof_detector.py --i eth0 # sniff on --i interface
			arp_spoof_detector.py # with default eth0
		"""
		),
	)
	parser.add_argument(
		"-i", "--interface", default="eth0", help="interface to sniff on"
	)
	values = parser.parse_args()
	return values


def getmac(ip):
	arp_request_header = scapy.ARP(pdst=ip)
	ether_header = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
	arp_request_packet = ether_header / arp_request_header
	answered_list = scapy.srp(arp_request_packet, timeout=1, verbose=False)[0]
	return answered_list[0][1].hwsrc


def sniff(interface):
	scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)


def process_sniffed_packet(packet):
	if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:
		try:
			real_mac = getmac(packet[scapy.ARP].psrc)
			response_mac = packet[scapy.ARP].hwsrc

			if real_mac != response_mac:
				print("[+] You are under attack!")

		except IndexError:
			pass


if __name__ == "__main__":

	options = get_args()
	sniff(options.interface)
