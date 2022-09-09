#!/usr/bin/env python3

import argparse  # https://docs.python.org/3/library/argparse.html
import os  # https://docs.python.org/3/library/os.html
import re  # https://docs.python.org/3/library/re.html
import subprocess  # https://docs.python.org/3/library/subprocess.html
import sys  # https://docs.python.org/3/library/sys.html
import textwrap  # https://docs.python.org/3/library/textwrap.html


def is_not_root():
    return os.geteuid() != 0


def get_args():
    parser = argparse.ArgumentParser(
        description="MAC address changer tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """Example: 
            mac_changer.py --i eth0 -m 00:11:11:11:22:55
        """
        ),
    )
    parser.add_argument(
        "-i", "--interface", default="eth0", help="interface to change MAC address for"
    )
    parser.add_argument(
        "-m", "--mac", default="52:54:00:99:3d:f3", help="new MAC address"
    )
    values = parser.parse_args()
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


if __name__ == "__main__":
    if is_not_root():
        sys.exit("[-] This script requires superuser privileges.")

    options = get_args()
    mac = get_mac(options.interface)
    print("[+] Current MAC address: " + str(mac))
    change_mac(options.interface, options.mac)
    mac = get_mac(options.interface)
    if mac == options.mac:
        print("[+] MAC address has changed to " + mac)
    else:
        print("[-] MAC address did not get changed.")
