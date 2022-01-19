#!/usr/bin/env python3

"""
For not missing the absolute basics, and for in strictly
confined environments w/o networking tools or compilers, 
copy/paste or connection to the internet.

See http://docs.python.org/3/library/socket.html

Assumptions:
* Connection will always succeed.
* The server expects us to be sent data first.
* The server will always return data in a timely fashion.
"""

import socket

target_host = "www.duckduckgo.com"
target_port = 80

# IP = "0.0.0.0"
# PORT = 9998

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

client.send(b"GET / HTTP/1.1\r\nHost:  duckduckgo.com\r\n\r\n")

# Receive some data
# The bufsize argument defines the maximum data it can
# receive at any one time.

response = client.recv(4096)
print(response.decode())
client.close()
