#!/usr/bin/env python2

# written by Moses Arocha
# Created with the help of "Black Hat Python" by Justin Seitz


import socket
import sys
import threading
import argparse


def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      # Creates a socket using IPv4 protocol and the TCP protocol
    try:
        server.bind((local_host, local_port))       # Creation of server
        print "\n [Success] Server Creation on %s:%d" % (local_host, local_port)
    except:
        print "\n [Failure] To Create Server on %s:%d" % (local_host, local_port)
        sys.exit(0)
    
    server.listen(5)
    
    while True:
        client_socket, addr = sever.accept()
        print "\n [Attempt] Received incomring connection from %s:%d" % (addr[0], addr[1])
        proxy_thread = threading.Thread(target=proxy_handler, args=(client_socket, remote_host, remote_port, receive_first))
        proxy_thread.start()

def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       # Creation of a socket using IPV4 and the TCP protocol
    remote_socket.connect((remote_host, remote_port))                       # Connection to 
    if receive_first:
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)
        remote_buffer = response_handler(remote_buffer)
        if len(remote_buffer)
            print " Sending Information To Local Host"
            len(remote_buffer)
            client_socket.send(remote_buffer)
    
    while True:
        local_buffer = receive_from(client_socket)
        if len(local_buffer):
                print " [A] Received %d Bytes From Local Host" % len(local_buffer)
                hexdump(local_buffer)
                local_buffer = request_handler(local_buffer)
                remote_socket.send(local_buffer)
                print " [A] Information Sent To Remote"
                
        remote_buffer = receive_from(remote_socket)
        
        if len(remote_buffer):
            print " [A] Received %d Bytes From Remote" % len(remote_buffer)
            hexdump(remote_buffer)
            remote_buffer = response_handler(remote_buffer)
            client_socket.send(remote_buffer)
            print " [A] Information Sent To Local Host"
            
        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()
            print " [A] Connection Will Close. Data Transmission Stopped"
            
            break

def hexdump(src, length=16):
    result = []
    digits = 4 if isinstance(src, unicode) else 2
    
    
    
def main():
    parser = argparse.ArgumentParser(description= "Usages For Program -h <Local Host>, -p <Local Port>, -r <Remote Host>, -x <Remote Port>, -f <Receive First>")
    parser.add_argument('-h', '--localhost', help='Please List The Local Host', type=str, action='local_host', required=True)
    parser.add_argument('-p', '--localport', help='Please List The Local Port', type=int, action='local_port', required=True)
    parser.add_argument('-r', '--remotehost', help='Please List The Remote Host', type=str, action='remote_host', required=True)
    parser.add_argument('-x', '--remoteport', help='Please List The Remote Port', type=int, action='remote_port', required=True)
    parser.add_argument('-f', '--receivefirst', help='Please List Whether To Recieve First or Not', type=str, action='receive_first', required=True)
    args = parser.parse_args()
