"""
Simple TCP proxy script (reading a message off one socket and 
slapping it on the other) for forwarding traffic to bounce from host 
to host, assessing network-based software, understanding unknown 
protocols, modifying traffic being sent to an application, and/or 
creating test cases for fuzzers.

Adopted and adapted from BlackHat 2021 and Gream
"""

# Socket pairs are iterated over until the right one is found
# Perhaps change to use a lookup instead of all of the looping

# Scaling (memory) concerns. Rethink the buffer where the whole 
# message is built before sending it to the message handler.

import argparse
import sys
import socket
import select
import threading
import binascii


class MessageProcessor:
    def handle_message(self, msg):
        pass


class HexDump(MessageProcessor):
    def handle_message(self, msg):
        print("[*] Message Hex:")
        print(binascii.b2a_hex(msg))


class ProxyServer:

    # Standard server set up, but with connection pairs for the client 
    # and server.
    def __init__(self, target_host, target_port, server_addr, server_port, handlers = []):
        self.__handlers = handlers
        self.__target_host = target_host
        self.__target_port = target_port
        self.__server_addr = server_addr
        self.__server_port = server_port
        self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__socket_pairs = []
        self.__close = False


    def run(self):
        self.__server_socket.bind((self.__server_addr, self.__server_port))
        self.__server_socket.listen(5)
        self.__reader_thread = threading.Thread(target=self.__reader_loop)
        self.__reader_thread.start()
        try:
            while True:
                client, addr = self.__server_socket.accept()
                print("[*] Accepted connection from {}".format(addr))
                target_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    target_sock.connect((self.__target_host, self.__target_port))
                    self.__socket_pairs.append((client, target_sock))
                except Exception as e:
                    print("[!!] Could not connect to target machine")
                    print(e)
                    client.shutdown(socket.SHUT_RDWR)
                    client.close()
        except KeyboardInterrupt:
            print("[!!] Caught keybboard interrupt. Closing down")
        except Exception as e:
            print("[!!] Caught exception")
            print(e)
        finally:
            self.__close = True
            self.__reader_thread.join()
            for (x,y) in self.__socket_pairs:
                x.shutdown(socket.SHUT_RDWR)
                x.close()
                y.shutdown(socket.SHUT_RDWR)
                y.close()
            self.__server_socket.shutdown(socket.SHUT_RDWR)
            self.__server_socket.close()


    def __reader_loop(self):
        while not self.__close:
            flatlist = [item for tempList in self.__socket_pairs for item in tempList]
            (rs, _, _) = select.select(flatlist, [], [], 0.1)
            for s in rs:
                matching_sock = None
                pair = None
                for (x, y) in self.__socket_pairs:
                    if x == s:
                        matching_sock = y
                        pair = (x,y)
                        print("[<==] Received message")
                        break
                    if y == s:
                        matching_sock = x
                        pair = (x,y)
                        print("[==>] Received message")
                        break
                raw_buffer = bytearray()
                while True:
                    (rss,_,_) = select.select([s], [], [], 0.001)
                    if len(rss) == 0:
                        break
                    raw_buffer.extend(s.recv(4096))
                if len(raw_buffer) == 0 or raw_buffer == b'\xff\xf4\xff\xfd\x06':
                    self.__socket_pairs.remove(pair)
                    s.shutdown(socket.SHUT_RDWR)
                    s.close()
                    matching_sock.shutdown(socket.SHUT_RDWR)
                    matching_sock.close()
                    continue
                for h in self.__handlers:
                    h.handle_message(raw_buffer)
                matching_sock.send(raw_buffer)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--client', default='127.0.0.1', dest='client', type=str, help='Address to bind to')
    parser.add_argument('-o', '--client-port', default=9001, dest='clientport', type=int, help='Port to bind to')
    parser.add_argument('-t', '--target', dest='target', required=True, type=str, help='Target address')
    parser.add_argument('-p', '--port', dest='targetport', required=True, type=int, help='Target port')
    parser.add_argument('-r', '--receive-first', type=bool, default=False, help='Receive first')
    return parser.parse_args(sys.argv[1:])


def main():
    """
    Create and start server object
    """
    args = parse_args()
    server = ProxyServer(args.target, args.targetport, args.client, args.clientport, [HexDump()])
    server.run()

# Main
if __name__ == "__main__":
    main()