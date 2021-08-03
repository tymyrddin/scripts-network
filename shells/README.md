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
    
