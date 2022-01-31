#!/usr/bin/env python3

import socket  # https://docs.python.org/3/library/socket.html

ip = "192.168.122.108"
port = 4444

listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Enable reuse of address
listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind to listen
listener.bind((ip, port))
listener.listen(0)
print("[+] Waiting for incoming connections.")
connection, address = listener.accept()
print("[+] Got a connection.")
