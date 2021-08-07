# Shells

## Netcat replacement

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
    
## Proxy

usage: proxy.py [-h] [-c CLIENT] [-o CLIENTPORT] -t TARGET -p TARGETPORT
                [-r RECEIVE_FIRST]
proxy.py: error: the following arguments are required: -t/--target, -p/--port

Note: Use sudo with port 21 because it is a privileged port, so listening on it
requires administrative or root privileges.

## SSH server and client

On one machine (for example a Windows machine) start the server:

    $ python ssh_server.py
    [+] Listening for connection ... 

On another machine start up the client:

    $ python ssh_client.py
    Password:

## SSH Proxy

The Paramiko demo files include a file called `rforward.py`. Run `rforward.py` from the Windows system and configure it to be the middleman to be able to tunnel traffic from a web server to the Kali SSH server.

    python rforward.py [SSH server address] -p 8081 -r [Web server address]:3000 --user=tim --password
    Enter SSH password:
    Connecting to ssh host [SSH server address]:22 . . .
    Now forwarding remote port 8081 to [Web server address]:3000 . . .
    
Now browse to http://127.0.0.1:8081 on the Linux server, and connect to the web server at
192.168.1.207:3000 through the SSH tunnel.

Flip back to the Windows machine to see the connection being made in Paramiko:

    Connected! Tunnel open ('127.0.0.1', 54690) -> ('SSH server address', 22) -> ('Web server address', 3000)