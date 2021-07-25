# sockstat 

sockstat is a tool to view information about open connections, sockets in use by GID, UID and process name, as well as the other criteria supported by FreeBSD's sockstat.

## Usage

View listening sockets:

    $ sudo sockstat -l
    USER     PROCESS              PID      PROTO  SOURCE ADDRESS            FOREIGN ADDRESS           STATE
    root     rpcbind              818      tcp4   *:*                       *:*                       LISTEN
    root     tor                  1060     tcp4   127.0.0.1:8960            *:*                       LISTEN
    root     exim4                1559     tcp4   127.0.0.1:*               *:*                       LISTEN


Use the grep command to select ports. To find out if port 22 and 80 are open or not:

    $ sudo sockstat -l | grep :22
    $ sudo sockstat -l | grep :80

Show only TCP sockets:

    $ sudo sockstat -P tcp

Show only UDP sockets:

    $ sudo sockstat -P udp

Both:

    $ sudo sockstat –P tcp,udp

Show TCP HTTPS port:

    $ sudo sockstat -P tcp -p 443

Show UDP DNS port:

    $ sudo sockstat -P udp -p 53

List opened and connected HTTPS ports:

    $ sudo sockstat -P tcp -p 443 -c
    USER     PROCESS              PID      PROTO  SOURCE ADDRESS            FOREIGN ADDRESS           STATE
    user     thunderbird          1947     tcp4   192.168.1.113:43008       68.333.166.118:993        ESTABLISHED

