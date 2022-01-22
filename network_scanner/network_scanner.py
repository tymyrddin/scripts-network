import argparse             # https://docs.python.org/3/library/argparse.html
import scapy.all as scapy   # https://scapy.readthedocs.io/en/latest/index.html


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="ip", help="IP address")
    values = parser.parse_args()
    if not values.ip:
        parser.error(
            "[-] Please specify a target IP address, use --help for more information"
        )
    return values


def scan(ip):
    # Create ARP broadcast request
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    # Send and receive
    answers = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    # Parse responses
    clients = []
    for answer in answers:
        client = {"ip": answer[1].psrc, "mac": answer[1].hwsrc}
        clients.append(client)
    return clients


def print_results(results):
    print("IP address\t\tMAC Address")
    print("-----------------------------------------")
    for result in results:
        print(result["ip"] + "\t\t" + result["mac"])
    print("-----------------------------------------")


# scan for example 192.168.122.1/24
options = get_args()
scan_results = scan(options.ip)
print_results(scan_results)
