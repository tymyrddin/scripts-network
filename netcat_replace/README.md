# Netcat replace

The utility knife of networking: read and write data across the network, meaning you can use it to execute
remote commands, pass files back and forth, or even open a remote shell. If a server allows python, well ... 
Useful for creating a simple network client and server to push files, or a listener giving command line access. 
If broken in through a web application, for dropping a Python callback to give secondary access without having to first burn a trojan or backdoor.

This is a basic version with limited functionality, and to be expanded on.

## Usage

```shell
usage: netcat.py [-h] [-c] [-e EXECUTE] [-l] [-p PORT] [-t TARGET] [-u UPLOAD]

Netcat replacement Tool

optional arguments:
  -h, --help            show this help message and exit
  -c, --command         command shell
  -e EXECUTE, --execute EXECUTE
                        execute specified command
  -l, --listen          listen
  -p PORT, --port PORT  specified port
  -t TARGET, --target TARGET
                        specified IP
  -u UPLOAD, --upload UPLOAD
                        upload file

Example: 
            netcat.py -t 192.168.1.108 -p 5555 -l -c # command shell
            netcat.py -t 192.168.1.108 -p 5555 -l -u=mytest.txt # upload file
            netcat.py -t 192.168.1.108 -p 5555 -l -e="cat /etc/passwd" # execute command
            echo 'ABC' | ./netcat.py -t 192.168.1.108 -p 135 # echo text to server port 135
            netcat.py -t 192.168.1.108 -p 5555 # connect to server
```

## Kick the Tyres

Play in the lab!