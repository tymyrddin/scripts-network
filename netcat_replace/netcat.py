#!/usr/bin/env python3

import argparse  # https://docs.python.org/3/library/argparse.html
import os  # https://docs.python.org/3/library/os.html
import shlex  # https://docs.python.org/3/library/shlex.html
import socket  # https://docs.python.org/3/library/socket.html
import subprocess  # https://docs.python.org/3/library/subprocess.html
import sys  # https://docs.python.org/3/library/sys.html
import textwrap  # https://docs.python.org/3/library/textwrap.html
import threading  # https://docs.python.org/3/library/threading.html


def is_not_root():
    return os.geteuid() != 0


# Receive and run a command; return the output as a string
def run_command(cmd):
    # Trim (newline)
    cmd = cmd.rstrip()
    if not cmd:
        return
    # Run a command on the local OS and returns the output from the command
    output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
    return output.decode()


# Create a command line interface and handle command line arguments
def get_args():
    # The -c , -e , and -u arguments imply the -l argument, because those arguments only apply
    # to the listener side of the communication. The sender side makes the connection to the
    # listener, and so it only needs the -t and -p arguments to define the target listener.
    parser = argparse.ArgumentParser(
        description="Netcat replacement tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """Example: 
            netcat.py -t 192.168.1.108 -p 5555 -l -c # command shell
            netcat.py -t 192.168.1.108 -p 5555 -l -u=mytest.txt # upload to file
            netcat.py -t 192.168.1.108 -p 5555 -l -e=\"cat /etc/passwd\" # execute command
            echo 'ABC' | ./netcat.py -t 192.168.1.108 -p 135 # echo text to server port 135
            netcat.py -t 192.168.1.108 -p 5555 # connect to server
        """
        ),
    )
    parser.add_argument("-c", "--command", action="store_true", help="command shell")
    parser.add_argument("-e", "--execute", help="execute specified command")
    parser.add_argument("-l", "--listen", action="store_true", help="listen")
    parser.add_argument("-p", "--port", type=int, default=5555, help="specified port")
    parser.add_argument("-t", "--target", default="192.168.1.203", help="specified IP")
    parser.add_argument("-u", "--upload", help="upload file")
    values = parser.parse_args()
    return values


class NetCat:

    # Initialize the NetCat object with the arguments from the command line
    # and the buffer and create the socket object
    def __init__(self, args, buffer=None):
        self.args = args
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):
        if self.args.listen:
            self.listen()
        else:
            self.send()

    def send(self):
        self.socket.connect((self.args.target, self.args.port))
        if self.buffer:
            self.socket.send(self.buffer)

        try:
            while True:
                recv_len = 1
                response = ""
                while recv_len:
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response += data.decode()
                    if recv_len < 4096:
                        break
                if response:
                    print(response)
                    buffer = input("> ")
                    buffer += "\n"
                    self.socket.send(buffer.encode())
        except KeyboardInterrupt:
            print("[+] \nDetected CTRL+C")
            self.socket.close()
            sys.exit()

    def listen(self):
        self.socket.bind((self.args.target, self.args.port))
        self.socket.listen(5)

        while True:
            client_socket, _ = self.socket.accept()
            client_thread = threading.Thread(target=self.handle, args=(client_socket,))
            client_thread.start()

    def handle(self, client_socket):

        if self.args.execute:
            output = run_command(self.args.execute)

            client_socket.send(output.encode())
        elif self.args.upload:
            file_buffer = b""
            while True:
                data = client_socket.recv(4096)
                if data:
                    file_buffer += data
                else:
                    break

            with open(self.args.upload, "wb") as f:
                f.write(file_buffer)
            message = f"[+] Saved file {self.args.upload}"
            client_socket.send(message.encode())

        elif self.args.command:
            cmd_buffer = b""
            while True:
                try:
                    client_socket.send(b"Netcat: #> ")
                    while "\n" not in cmd_buffer.decode():
                        cmd_buffer += client_socket.recv(64)
                    response = run_command(cmd_buffer.decode())
                    if response:
                        client_socket.send(response.encode())
                    cmd_buffer = b""
                except Exception as e:
                    print(f"[-] Server killed {e}")
                    self.socket.close()
                    sys.exit()


if __name__ == "__main__":
    if is_not_root():
        sys.exit("[-] This script requires superuser privileges.")

    options = get_args()
    if options.listen:
        # If as listener, invoke the NetCat object with an empty buffer string
        setbuffer = ""
    else:
        # Otherwise, send the buffer content from stdin
        setbuffer = sys.stdin.read()

    nc = NetCat(options, setbuffer.encode())
    # Start it up
    nc.run()
