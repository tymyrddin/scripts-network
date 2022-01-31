# Client-server skeleton

For not missing the absolute basics, and in for in strictly confined environments w/o networking tools or compilers, copy/paste or connection to the internet.

Assumptions:
* Connection will always succeed.
* The server expects us to be sent data first.
* The server will always return data in a timely fashion.

## Requirements

* Python 3, Root access, sockets and threading modules

## Scripts

- [x] A standard multi-threaded [TCP server](tcp_server.py): Can be expanded on for writing command shells or coding a proxy.
- [x] [TCP client](tcp_client.py)
- [x] [UDP client](udp_client.py)

## Kicking the Tyres

In one terminal run the server script:

```shell
$ python tcp_server.py    
[*] Listening on 0.0.0.0:9998
```

Then start the client script in the Windows VM:

```shell
$ python tcp_client.py
ACK
```

Server terminal now looks like:

```shell
$ python tcp_server.py    
[*] Listening on 0.0.0.0:9998
[*] Accepted connection from 127.0.0.1:55148
[*] Received: Hello Server
```

