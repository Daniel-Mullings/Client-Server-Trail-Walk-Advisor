#!/usr/bin/env python
# Python Network Programming Cookbook,Second Edition -- Chapter - 1

import socket
import sys

host = '127.0.0.1'
port = 12345
data_payload = 2048
backlog = 5

'''A simple echo server'''
def echo_server(p_port):
    # Create a TCP socket
    sock = socket.socket(socket.AF_INET, 
                          socket.SOCK_STREAM)
    
    #Enable reuse address/port 
    sock.setsockopt(socket.SOL_SOCKET, 
                      socket.SO_REUSEADDR, 1)
    
    #Bind the socket to the port
    #Print ("Starting up echo server on %s port %s" % server_address)
    sock.bind(('127.0.0.1', p_port))
    
    #Listen to clients, backlog argument specifies the max No. of queued connections
    sock.listen(backlog) 
    while True: 
        print ("Server standby to receive message from client. . .")
        client, address = sock.accept() 
        data = client.recv(data_payload)
        print("Message Received form client: ",data)
        if data:
            data=data.upper()
            print ("Data to Send to Client: %s" %data)
            client.send(data)
            print ("sent %s bytes back to %s" % (data, address))
        
        #End connection
        client.close() 
    
if __name__ == '__main__':
    #Given_args = parser.parse_args() 
    port = 12345
    echo_server(port)