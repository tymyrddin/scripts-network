# Getting started

Creating TCP servers in Python is just as easy as creating a client.

## The scripts

In one terminal with the virtual environment activated run the [tcp_server.py](tcp_server.py) script:

    $ python tcp_server.py    
    [*] Listening on 0.0.0.0:9998

Then start the [tcp_client.py](tcp_client.py) script in another terminal (also with the virtual environment activated):

    $ python tcp_client.py
    ACK

Server terminal now looks like:

    $ python tcp_server.py    
    [*] Listening on 0.0.0.0:9998
    [*] Accepted connection from 127.0.0.1:55148
    [*] Received: Hello Server