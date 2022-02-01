# Netcat replace

The utility knife of networking: read and write data across the network, meaning you can use it to execute
remote commands, pass files back and forth, or even open a remote shell. If a server allows python, well ... 
Useful for creating a simple network client and server to push files, or a listener giving command line access. 
If [broken in through a web application](https://github.com/tymyrddin/reomais), useful for dropping a Python callback to give secondary access without having to first burn a trojan or backdoor.

This is a basic version with limited functionality, using a buffer protocol for serialization.

## Usage

```shell
usage: netcat.py [-h] [-c] [-e EXECUTE] [-l] [-p PORT] [-t TARGET] [-u UPLOAD]

Netcat replacement tool

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

the script reads from stdin and will do so until it receives the end-of-file (EOF) marker. 
To send EOF, press CTRL-D on your keyboard.

## Kicking the Tyres

On Kali set up a listener using its own IP and port 4444 to provide a command shell:

```shell
@kali:~$ sudo python3 netcat.py -t 192.168.122.108 -p 4444 -l -c
```

Also on Kali, in another terminal, run the script in client mode:

```shell
@kali:~$ sudo python3 netcat.py -t 192.168.122.108 -p 4444
[sudo] password for <user>: 

```

Do CTRL-D to get the prompt:

```shell
Netcat: #> 
> ls -la
total 348
drwxr-xr-x  2 nina nina   4096 Feb  1 15:56 .
drwxr-xr-x 19 nina nina   4096 Feb  1 11:50 ..
-rw-r--r--  1 nina nina 219285 Feb  1 04:28 love.jpg
-rw-r--r--  1 nina nina   5779 Feb  1 12:05 netcat.py
-rw-r--r--  1 nina nina 113974 Feb  1 04:28 portrait.jpg
-rw-r--r--  1 nina nina   2033 Feb  1 15:56 README.md
Netcat: #> 
> 
```