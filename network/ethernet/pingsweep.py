"""A simple script for finding live hosts by using ping sweep.
Authors: Reinica and Nina

Ping sweep is used for various purposes, such as improving and maintaining network security by
identifying IP addresses used by “live” or “dead” hosts. These hosts are typically computers,
but anything can be a host, including printers, computer systems, websites, networks, and devices.
Ping sweeps can also be used to detect rogue devices connected to the network!

Ping sweeps are nothing more than a knock on a door, and are allowed.
Note that personal and general firewalls are often set to a so-called
“stealth mode” which is used not to react to ICMP echo requests.

Python requires root to spawn ICMP (i.e. ping) sockets in linux.
Call this script with sudo or as superuser."""

import argparse
import time
import ipaddress                # https://docs.python.org/3/library/ipaddress.html
import subprocess
import platform
import socket


def parse_arguments():
    parser = argparse.ArgumentParser(description='Process command line arguments.')
    parser.add_argument("-i",
                        "--ip",
                        help="A network address in CIDR format",
                        type=is_valid_networkaddress,
                        default='127.0.0.1')
    return parser.parse_args()


def is_valid_networkaddress(ip):
    try:
        ipaddress.ip_address(ip)
        return ip
    except socket.error:
        raise argparse.ArgumentTypeError(f"{ip} is not a valid IP address")


def setoscommand():
    # Select ping sweep command according to platform

    operating_system = platform.system()
    if operating_system == "Windows":
        cmd = "ping -n "
    elif operating_system == "Linux":
        cmd = "ping -c "
    else:
        cmd = "ping -c "
    return cmd


def makebase(ip):
    # Get the first three octets and add a .

    ip_net = ip.split('.')
    a = '.'
    base_net = ip_net[0] + a + ip_net[1] + a + ip_net[2] + a
    return base_net


def sweep(ip):
    # Send ICMP ECHO request and verify response status

    cmd = setoscommand()
    base_net = makebase(ip)

    starttime = time.time()
    print("Scanning in progress: ")

    for ip in range(1, 255):
        address = base_net + str(ip)
        sp = subprocess.Popen(cmd + address,
                              shell=True,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)

        # Store the return code in rc variable
        # rc = sp.wait()

        # Separate the output and error by communicating with sp variable.
        out, err = sp.communicate()

        # print('Return Code:', rc, '\n')
        # print('output is: \n', out)
        # print('error is: \n', err)

        if out == 0:
            print(address + "--> Live")
        else:
            print(address + "--> No response")

    print("Scanning completed in: ", time.time() - starttime)


def main():
    parsed_args = parse_arguments()

    if parsed_args.ip:
        sweep(parsed_args.ip)


# Execute
if __name__ == '__main__':
    main()
