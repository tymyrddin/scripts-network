"""
For not missing the absolute basics, and in for in strictly 
confined environments w/o networking tools or compilers, 
copy/paste or connection to the internet.

See http://docs.python.org/3/library/socket.html
"""

import socket
import threading


# IP address and port we want the server to listen on
IP = "0.0.0.0"
PORT = 9998


def main():
    # IPv4 TCP connection
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to the IP and port number
    server.bind((IP, PORT))
    # Listen to the connection and wait for the client
    # Maximum backlog of connections set to 5
    server.listen(5)
    print(f"[*] Listening on {IP}:{PORT}")

    while True:
        # The accept() method returns two values: client socket and address.
        client, address = server.accept()
        print(f"[*] Accepted connection from {address[0]}:{address[1]}")
        # Create a new thread object that points to the
        # handle_client function, and pass it the client socket object
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()


def handle_client(client_socket):
    with client_socket as sock:
        request = sock.recv(1024)
        print(f'[*] Received: {request.decode("utf-8")}')
        sock.send(b"ACK")


# Main
if __name__ == "__main__":
    main()
