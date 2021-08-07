"""Imagine having remote access to an SSH server on an internal network, 
but no direct access to the web server on the same network. The
server with SSH installed does have access, but this SSH server doesn’t have
the tools we'd like to use.

One way to overcome this problem is to set up a forward SSH tunnel.
    ssh -L 8008:web:80 username@sshserver

Alas, not many Windows systems are running an SSH server service. 
Instead, configure a reverse SSH tunneling connection: Set up
an SSH server on attack machine and connect back to it from the Windows
client and through that SSH connection, specify a remote port on the 
SSH server that gets tunneled to the local host and port.

These then can be used to expose port 3389 to access an internal system 
using Remote Desktop or to access another system that the Windows client 
can access (like the web server).

The Paramiko demo files include a file called rforward.py that does
exactly this (transport mode of Paramiko).

Adopted and adapted from BlackHat 2021
"""

# Future development: None
# In theory we could intercept the socket reads and writes messages and 
# add to these as we want.

import threading
import socket
import select
import getpass
import argparse
import sys
import time

import paramiko

verbose_enabled = False

def verbose(message):
    if verbose_enabled:
        print(message)


def parse_options(argv):
    args = argparse.ArgumentParser()
    args.add_argument('-password', '-a', dest='password', action='store_true', default=False)
    args.add_argument('-verbose', '-v', dest='verbose', action='store_true', default=False)
    args.add_argument('-user', '-u', type=str, dest='user')
    args.add_argument('-bindaddr', '-b', type=str, dest='bindaddr', default='127.0.0.1')
    args.add_argument('-bindport', '-p', type=int, dest='bindport', default=8080)
    args.add_argument('-remoteaddr','-r', type=str, dest='remoteaddr')
    args.add_argument('-remoteport', '-o', type=int, dest='remoteport', default=22)
    args.add_argument('-keyfile', '-k', type=str, dest='keyfile')
    args.add_argument('-lookforkeys', '-l', dest='lookforkeys', action='store_true', default=False)
    return args.parse_args(argv)


def main():
    args = parse_options(sys.argv[1:])
    if args.remoteaddr is None:
        print('Remote address is a required argument')
        sys.exit(1)
    if args.remoteport is None:
        print('Remote port is a required argument')
        sys.exit(1)
    if args.user is None:
        print('SSH User is a required argument')
        sys.exit(1)
    global verbose_enabled
    verbose_enabled = args.verbose
    password = None
    if args.password:
        password = getpass.getpass('Enter SSH password: ')
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())
    verbose('Connecting to ssh host %s:%d ...' % (args.remoteaddr, args.remoteport))
    try:
        client.connect(args.remoteaddr, args.remoteport, username=args.user, key_filename=args.keyfile, look_for_keys=args.lookforkeys, password=password)
    except Exception as e:
        print('*** Failed to connect to %s:%d: %r' % (args.remoteaddr, args.remoteport, e))
        sys.exit(1)
        verbose('Now forwarding remote port {} to {}:{} ...'.format(args.bindport, args.remoteaddr, args.remoteport))
    try:
        reverse_forward_tunnel(args.bindport, args.remoteaddr, args.remoteport, client.get_transport())
    except KeyboardInterrupt:
        print('C-c: Port forwarding stopped.')
    sys.exit(0)


def reverse_forward_tunnel(server_port, remote_host, remote_port, transport):
    transport.request_port_forward('', server_port)
    while True:
        chan = transport.accept(1000)
        if chan is None:
            continue
        thr = threading.Thread(target=handler, args=(chan, remote_host, remote_port))
        thr.setDaemon(True)
        thr.start()


def handler(chan, host, port):
    sock = socket.socket()
    try:
        sock.connect((host, port))
    except Exception as e:
        verbose('Forwarding request to %s:%d failed: %r' % (host, port, e))
        return
    verbose('Connected! Tunnel open %r -> %r -> %r' % (chan.origin_addr, chan.getpeername(), (host, port)))
    while True:
        r, w, x = select.select([sock, chan], [], [])
        if sock in r:
            data = sock.recv(1024)
            if len(data) == 0:
                break
            chan.send(data)
        if chan in r:
            data = chan.recv(1024)
            if len(data) == 0:
                break
            sock.send(data)
    chan.close()
    sock.close()
    verbose('Tunnel closed from %r' % (chan.origin_addr,))


if __name__ == "__main__":
    main()