#!/usr/bin/env python 
# Source Python Network Programming Cookbook,Second Edition -- Chapter - 1 
 
import socket 
import sys
import argparse
 
host = '127.0.0.1'

def echo_client(p_port): 
    """ A simple echo client """ 
    #Create a TCP/IP socket 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    
    #Connect the socket to the server 
    #server_address = ('127.0.0.1', 12345)
    print("--------------------")
    
    #Print (Connecting to %s port %s" % server_address) 
    #sock.connect(server_address)
    sock.connect((host, p_port))

    #Send data 
    try:
        #Send data
        message = input("Enter your query: ")
        print ("\Request to Server: \"%s\"" % message) 
        sock.sendall(message.encode('utf-8')) 
        
        #Look for the response 
        amount_received = 0 
        amount_expected = len(message) 
        while amount_received < amount_expected: 
            data = sock.recv(1024) 
            amount_received += len(data) 
            print ("Reponse from Server: ", data.decode("utf-8"))
    except socket.error as e: 
        print ("\nSocket error: %s" %str(e)) 
    except Exception as e: 
        print ("\nOther exception: %s" %str(e)) 
    finally: 
        print ("\nClosing connection to the server") 
        sock.close() 

if __name__ == '__main__': 
    port = 12345 
    while True:
        echo_client(port)