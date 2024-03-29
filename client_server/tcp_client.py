#!/usr/bin/env python3

import socket  # https://docs.python.org/3/library/socket.html


target_host = "192.168.122.108"
target_port = 4444

# Create a socket object using the socket.socket() function of
# the socket module. General syntax:
#   s = socket.socket (socket_family, socket_type, protocol=0)
# with socket_family: socket.AF_INET (the address family for IPv4),
# and socket_type: socket.SOCK_STREAM (TCP is reliable and a two-way,
# connection-based service)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the client
# The address argument of the method is the address of the server

client.connect((target_host, target_port))

# Send some data as bytes.
# The method returns the number of bytes sent.

# client.send(b"GET / HTTP/1.1\r\nHost:  duckduckgo.com\r\n\r\n")
client.send(b"Hello Server")

# Receive some data
# The bufsize argument defines the maximum data it can
# receive at any one time.

response = client.recv(4096)
print(response.decode())
client.close()
