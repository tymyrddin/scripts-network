#!/usr/bin/env python3

import socket  # https://docs.python.org/3/library/socket.html

target_host = "127.0.0.1"
target_port = 9997

# Create a socket object using the socket.socket() function of
# the socket module. General syntax:
#   s = socket.socket (socket_family, socket_type, protocol=0)
# with socket_family: socket.AF_INET (the address family for IPv4),
# and socket_type: socket.SOCK_DGRAM (UDP is unreliable and
# connectionless)

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Send some data as bytes.
# The method returns the number of bytes sent.

client.sendto(b"Nonsense", (target_host, target_port))

# Receive some data (and details of the remote host and port)
# The bufsize argument defines the maximum data it can
# receive at any one time.

data, addr = client.recvfrom(4096)
print(data.decode())
client.close()
