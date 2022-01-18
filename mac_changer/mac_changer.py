#! /usr/bin/env python

import subprocess
import argparse
import re


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--interface",
        dest="interface",
        help="interface to change MAC address for",
    )
    parser.add_argument("-m", "--mac", dest="new_mac_address", help="new MAC address")
    values = parser.parse_args()
    if not values.interface:
        parser.error("[-] Please specify an interface, use --help for more information")
    if not values.new_mac_address:
        parser.error(
            "[-] Please specify a new MAC address, use --help for more information"
        )
    return values


def change_mac(interface, new_mac_address):
    print("[+] Changing MAC address for " + interface + " to " + new_mac_address)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac_address])
    subprocess.call(["ifconfig", interface, "up"])


def get_mac(interface):
    ifconfig_results = subprocess.check_output(["ifconfig", interface])
    mac_search_results = re.search(
        r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_results)
    )
    if mac_search_results:
        return mac_search_results.group(0)
    else:
        print("[-] No MAC address found for this interface")


options = get_args()
mac = get_mac(options.interface)
print("[+] Current MAC address: " + str(mac))
change_mac(options.interface, options.new_mac_address)
mac = get_mac(options.interface)
if mac == options.new_mac_address:
    print("[+] Success. MAC address has changed to " + mac)
else:
    print("[-] MAC address did not get changed.")
