'''Query Builder: 
----------------------------------------------------------------------------------
   Search Query:
   
   Structure:     [action] {[minLengthInMiles] [maxLengthInMiles] [difficulty]}
                           ^      Section repeated as chain for multiple      ^
                                           simultaneous searche

   Examples:      [search] {[PeakDistrict] [6] [8] [Easy]}
                  [search] {[PeakDistrict] [6] [8] [Easy]} {[York] [5] [9] [Hard]}
----------------------------------------------------------------------------------
   Buy Query:

   Structure:     [action] {[customerName] [bookNum] [quantity]}
                           ^   Section repeated as chain for   ^
                               multiple simultaneous searches

   Examples:      [buy] {[John Smith] [101] [1]}
                  [buy] {[John Smith] [101] [1]} {[Mike Pence] [102] [2]}
----------------------------------------------------------------------------------
'''

import socket                                                               #Import "socket" Python module
import sys                                                                  #Import "sys" Python module

#List containing list cataloguing nature walks in books
walks = [#Area            Dist Diff      Book Name                   Walk Name            Pg
         ["PeakDistrict", 7,   "Easy",   "More Peak District",       "Hathasage",         67],
         ["PeakDistrict", 4.5, "Medium", "More Peak District",       "Hope and Win Hill", 18],
         ["Lincolnshire", 3.5, "Easy",   "Lincolnshire Wolds",       "Thornton Abbey",    20],
         ["Lincolnshire", 5,   "Hard",   "Lincolnshire Wolds",       "Tennyson County",   28],
         ["York",         8,   "Hard",   "Vale of York",             "Cowlam and Cotham", 64],
         ["York",         7,   "Easy",   "Vale of York",             "Fridaythorpe",      42],
         ["PeakDistrict", 4.5, "Medium", "Peak District",            "Magpie Mine",       20],
         ["PeakDistrict", 5.5, "Easy",   "Peak District",            "Lord's Seat",       28],
         ["NorthWales",   4,   "Hard",   "Snowdonia",                "Around Aber",       24],
         ["NorthWales",   3.5, "Medium", "Snowdonia",                "Yr Eifl",           42],
         ["Warwickshire", 4,   "Easy",   "Malvern and Warwickshire", "Edge Hill",         28],
         ["Warwickshire", 8.5, "Medium", "Malvern and Warwickshire", "Bidford-Upon-Avon", 78],
         ["Cheshire",     5,   "Easy",   "Cheshire",                 "Dane Valley",       20],
         ["Cheshire",     8.5, "Medium", "Cheshire",                 "Malpas",            80],
         ["Cheshire",     6,   "Hard",   "Cheshire",                 "Farndon",           48],
         ["Cheshire",     5.5, "Easy",   "Cheshire",                 "Delamere Forest",   30]
        ]

#List containing list cataloguing book details
books = [#Book Name                   No.    Price
         ["More Peak District",       "101", "12.99"],
         ["Lincolnshire Wolds",       "102", "10.99"],
         ["Vale of York",             "103", "11.99"],
         ["Peak District",            "104", "12.99"],
         ["Snowdonia",                "105", "13.99"],
         ["Malvern and Warwickshire", "106", "10.99"],
         ["Cheshire",                 "107", "12.99"]
        ]

host = '127.0.0.1'
port = 12345
data_payload = 2048
backlog = 5



'''Define function called "echoServer": Implements client/server communication
   Input:  "p_host" = localhost address, "p_port" = localhost port
   Output: Gernerate/Respond to client request

   REFERENCE: Python Network Programming Cookbook, Second Edition -- Chapter - 1 
'''
def echoServer(p_host, p_port):
    # Create a TCP socket
    sock = socket.socket(socket.AF_INET, 
                          socket.SOCK_STREAM)
    
    #Enable reuse address/port 
    sock.setsockopt(socket.SOL_SOCKET, 
                      socket.SO_REUSEADDR, 1)
    
    #Bind the socket to the port
    #Print ("Starting up echo server on %s port %s" % server_address)
    sock.bind((p_host, p_port))
    
    #Listen to clients, backlog argument specifies the max No. of queued connections
    sock.listen(backlog) 
    while True: 
        print ("Server standing by to receive request from client. . .")
        
        #Receive client request
        client, address = sock.accept() 
        query = client.recv(data_payload).decode().lower()
        print("\nRequest from Client: \"%s\"" % query)

        #Send client response
        reponse = queryReponse(query).encode()
        print("Response to Client: %s" %reponse.decode())
        client.send(reponse)
        print("Server Sent: %s, bytes back to %s\n" % (reponse, address))
        
        #End connection
        client.close() 



'''Define function called "getQueryAction": Implements determining intended query action
   Input:  "p_query" = Query from client
   Output: 
'''
def getQueryAction(p_query):
    queryAsComponents = p_query.split()                                     #Store each word in "p_query" as seperate element in "queryAsComponents" list
    action = queryAsComponents[0]                                           #Determine intended query action contained in initial word in "p_query", now '0'-th element of "queryAsComponents", assign to "action"
    return action                                                           #Return "action" to caller

'''Define function called "queryReponse": Implements generating response to client query
   Input:  "p_query" = Query from client
   Output: Returns string, containing response to client query
'''
def queryReponse(p_query):
    if getQueryAction(p_query) == "search":                                 #If return value of "getQueryAction()" equal to "search"
        return qeurySearch(p_query)                                         #Return, return value qeurySearch() to subsequent caller of "queryResponse()"
    elif getQueryAction(p_query) == "buy":                                  #If return value of "getQueryAction()" equal to "search"
        return qeuryBuy()                                                   #Return, return value qeuryBuy() to subsequent caller of "queryResponse()"
    return "Invalid Query\n"                                                #Return string to subsequent caller of "queryResponse()"

                                                                            #NOTE: Subsequent caller of "queryResponse()" is "echoServer()", 
                                                                            #return value returned/printed as reponse to client query

'''Define function called "querySearch: Implements generating results for query search against catalogued nature walks in books
   Input:  "p_query" = Query from client
   Output: Returns "message", containing details of catalogued nature walks in books and book details that match query search criteria
'''
def qeurySearch(p_query):
    queryAsCompentents = p_query.split()                                    #Each word in "p_query" as element in "queryAsComponent"
    queryAsCompentents.pop(0)                                               #Remove initial element in "queryAsCompnent", which represents query action
    
    searchRequests = []                                                     #Store list of search requests for walks matching criteria
    walksFound = []                                                         #Store list of walks found in "walks" matching criteria of elements in "searchRequests"

    #Populate "searchRequests" with lists containing search parameters for search  requests provided in "queryAsCompentents"
    #NOTE: A single search request takes four consecutive elements in "queryAsCompentents" to construct a single search request
    #NOTE: Reference "Query Builder" at top of "server.py"
    for index in range(0, len(queryAsCompentents), 4):
        searchRequests.append(queryAsCompentents[index:index+4])

    #For each "searchRequest" in "searchRequests"
    for searchRequest in searchRequests:
        #For each "walk" in "walks", check is any "searchRequest" equal to "walk" (i.e. Match search request criteria)
        for walk in walks:
            if ((str(searchRequest[0]).lower() == str(walk[0]).lower()) and #Check if "searchRequest" "area" equal to "walk" "Area"
                (float(searchRequest[1]) <= float(walk[1])) and             #Check if "searchRequest" "minLengthInMiles" <= "walk" "Dist"
                (float(searchRequest[2]) >= float(walk[1])) and             #Check if "searchRequest" "maxLengthInMiles" >= "walk" "Dist"
                (str(searchRequest[3]).lower() == str(walk[2]).lower())):   #Check if "searchRequest" "difficulty" >= "walk" "Diff"
                    walksFound.append(walk)                                 #If all criteria match, store list "walk" details in "walksFound" list
    
    #Construct formatted return message containing walks found matching query search criteria
    if len(walksFound) > 0:                                                 #If walksFound contains non-empty list (i.e. Walks found that match search request criteria)
        message = "\n\nThe following walks were found:\n\n"                 #Inital message w/ header, content to be concatenated
        counter = 1                                                         #Counter to concatenate numerical bulletpoints to list of walks
        for walk in walksFound:                                             #For each "walk" in "walksFound"
            tempStr = (str(counter) + ") " +                                #Create "tempStr" (Temporary String) w/ numerical bulletpoint using "counter", concatenate
                       "Book Name: " + str(walk[4]).capitalize() +          #Book name from "walk" in "walksFound", concatenate
                       ", Walk Name: " + str(walk[3]).capitalize()  +       #Walk name from "walk" in "walksFound", concatenate
                       ", Pg.: " + str(walk[5]) + '\n')                     #Page number from "walk" in "walksFound", concatenate
            message += tempStr                                              #Set "Message" value to existing message value plus "tempStr" value
            counter += 1                                                    #Increment counter by 1

        return message                                                      #Return "Message", after "for" loop concatenates all walks that match search request criteria
    
    message = "No walks matching criteria were found\n"                     #Set "Message" if previous "if" statement not executed as no walks 
                                                                            #that match search request criteria identified
    return message                                                          #Return "Message"

'''Define function called "queryBuy: Implements buying books and generating order details
   Input:  "p_query" = Query from client
   Output: N/A
'''
def qeuryBuy():
    #IMPLEMENT
    return "Buy in Development"



if __name__ == '__main__':
    #Given_args = parser.parse_args() 
    echoServer(host, port)