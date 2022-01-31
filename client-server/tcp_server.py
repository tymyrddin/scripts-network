#!/usr/bin/env python3

import socket  # https://docs.python.org/3/library/socket.html
import threading  # https://docs.python.org/3/library/threading.html


# IP address and port we want the server to listen on
ip = "192.168.122.108"
port = 4444


def main():
    # IPv4 TCP connection
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Enable reuse of address
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Bind the socket to the IP and port number
    server.bind((ip, port))
    # Listen to the connection and wait for the client
    # Maximum backlog of connections set to 5
    server.listen(5)
    print(f"[+] Listening on {ip}:{port}")

    while True:
        # The accept method returns two values: client socket and address.
        client, address = server.accept()
        print(f"[+] Accepted connection from {address[0]}:{address[1]}")
        # Create a new thread object that points to the
        # handle_client function, and pass it the client socket object
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()


def handle_client(client_socket):
    with client_socket as sock:
        request = sock.recv(1024)
        print(f'[+] Received: {request.decode("utf-8")}')
        sock.send(b"ACK")


# Main
if __name__ == "__main__":
    main()
