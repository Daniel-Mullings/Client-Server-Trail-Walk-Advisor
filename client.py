import socket 
import sys
import argparse
 
host = '127.0.0.1'
port = 12345 

'''Define function called "echoClient": Implements client/server communication
   Input:  "p_host" = localhost address, "p_port" = localhost port
   Output: Receive/Display server response

   REFERENCE: Python Network Programming Cookbook, Second Edition -- Chapter - 1 
'''
def echoClient(p_host, p_port): 

    #Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    
    #sock.connect(server_address) (server_address = '127.0.0.1', 12345)
    sock.connect((p_host, p_port))

    #Try: Sending/Receiving server Requests/Responses 
    try:
        #Get user query
        print(str("-"*75))
        message = input("Enter your query: ").lower()

        #Send server request
        print("\nRequest to Server: \"%s\"" % message) 
        sock.sendall(message.encode('utf-8')) 
        
        #Receive server response 
        data = sock.recv(1024)
        print("Reponse from Server:", data.decode("utf-8"))

    #Handle: Exception
    except socket.error as e: 
        print("Socket error: %s" %str(e))
    except Exception as e: 
        print("Other exception: %s" %str(e)) 
    finally: 
        print("Closing connection to Server") 
        sock.close() 



if __name__ == '__main__': 
    while True:
        echoClient(host, port)