'''Query Builder: 
----------------------------------------------------------------------------------
   Search Query:
   
   Structure:     [action] {[minLengthInMiles] [maxLengthInMiles] [difficulty]}
                           ^      Section repeated as chain for multiple      ^
                                           simultaneous search

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

host = '127.0.0.1'
port = 12345
data_payload = 2048
backlog = 5

#List containing list walks from books
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
books = [#Book Name                   Bk No. Price
         ["More Peak District",       "101", "12.99"],
         ["Lincolnshire Wolds",       "102", "10.99"],
         ["Vale of York",             "103", "11.99"],
         ["Peak District",            "104", "12.99"],
         ["Snowdonia",                "105", "13.99"],
         ["Malvern and Warwickshire", "106", "10.99"],
         ["Cheshire",                 "107", "12.99"]
        ]



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
        print(str("-"*100))
        print ("Server standing by to receive request from client. . .")
        
        #Receive client request
        client, address = sock.accept() 
        query = client.recv(data_payload).decode().lower()
        print("\nRequest from Client: \"%s\"" % query)

        #Send client response
        response = queryResponse(query).encode()
        print("Response to Client: %s" %response.decode())
        client.send(response)
        print("Server Sent: %s, bytes back to %s\n" % (response, address))
        
        #End connection
        client.close() 



'''Define function called "getQueryAction": Implements determining intended query action
   Input:  "p_query" = Query from client
   Output: 
'''
def getQueryAction(p_query):
    queryAsComponents = p_query.split()                                     #Store whitespace separated words in "p_query" in "queryAsComponents" list
    action = queryAsComponents[0]                                           #Set "action" to '0'-th element of "queryAsComponents", determine intended query action
    return action                                                           #Return "action" to caller

'''Define function called "queryReponse": Implements generating response to client query
   Input:  "p_query" = Query from client
   Output: Returns string, containing response to client query
'''
def queryResponse(p_query):
    if getQueryAction(p_query) == "search":                                 #If "getQueryAction()" return value equal to "search"
        return querySearch(p_query)                                         #Return "querySearch()" return value to subsequent caller of "queryResponse()"
    elif getQueryAction(p_query) == "buy":                                  #If "getQueryAction()" return value equal to "buy"
        return queryBuy(p_query)                                            #Return, "queryBuy()" return value to subsequent caller of "queryResponse()"
    return "Invalid Query\n"                                                #Return string literal to subsequent caller of "queryResponse()"

                                                                            #NOTE: Subsequent caller of "queryResponse()" is "echoServer()", 
                                                                            #      "queryResponse()" return values returned/printed as server reponse to client query

'''Define function called "querySearch: Implements generating results for query search criteria for walks in books
   Input:  "p_query" = Query from client
   Output: Returns "message", containing results of walks from books that match query search criteria
'''
def querySearch(p_query):
    queryAsCompentents = p_query.split()                                    #Store whitespace separated words in "p_query" in "queryAsComponent"
    queryAsCompentents.pop(0)                                               #Remove '0'-th element in "queryAsCompnent", represents query action
    
    searchRequests = []                                                     #Store list of search requests for walks matching criteria
    walksFound = []                                                         #Store list of walks found in "walks" matching criteria of "searchRequests"

    #Populate "searchRequests" with lists containing search parameters for search requests provided by "queryAsCompentents"
    #NOTE: A single search request takes four consecutive elements from "queryAsCompentents" to construct a single search request
    #      Reference "Query Builder" at top of "server.py"
    for index in range(0, len(queryAsCompentents), 4):
        searchRequests.append(queryAsCompentents[index:index+4])

    #For each "searchRequest" in "searchRequests"
    for searchRequest in searchRequests:
        #For each "walk" in "walks", check if any "searchRequest" equal to "walk" (i.e. Match search request criteria)
        for walk in walks:
            if ((str(searchRequest[0]).lower() == str(walk[0]).lower()) and #If "searchRequest" "area" equal to "walk" "Area"
                (float(searchRequest[1]) <= float(walk[1])) and             #If "searchRequest" "minLengthInMiles" less than or equal to "walk" "Dist"
                (float(searchRequest[2]) >= float(walk[1])) and             #If "searchRequest" "maxLengthInMiles" greater than or equal to "walk" "Dist"
                (str(searchRequest[3]).lower() == str(walk[2]).lower())):   #If "searchRequest" "difficulty" equal to "walk" "Diff"
                    walksFound.append(walk)                                 #If all criteria match, store list "walk" details in "walksFound" list
    
    #Construct formatted return message containing numerical list walks found matching query search criteria
    if len(walksFound) > 0:                                                 #If "walksFound" is non-empty list (i.e. Walks found that match search request criteria)
        message = "\n\nThe following walks were found:\n"                   #Set "message" to initial  header, concatenated content contains walk details
        counter = 1                                                         #Counter to concatenate numerical bulletpoints to list of walks
        for walkFound in walksFound:                                        #For each "walk" in "walksFound"
            tempStr = (str(counter) + ") " +                                #Create "tempStr" (Temporary String) w/ numerical bulletpoint using "counter", concatenate
                       "Book Name: " + str(walkFound[4]).capitalize() +     #Book name from "walkFound" in "walksFound", concatenate
                       ", Walk Name: " + str(walkFound[3]).capitalize()  +  #Walk name from "walkFound" in "walksFound", concatenate
                       ", Pg.: " + str(walkFound[5]) + '\n')                #Page number from "walkFound" in "walksFound", concatenate

            counter += 1                                                    #Increment "counter" by 1
            message += tempStr                                              #Concatenate "tempStr" to "message"
        
        return message                                                      #Return "message"
    
    message = "No walks matching search criteria found\n"                   #"message" set to literal string detailing no search requests criteria match walks
    return message                                                          #Return "message" to caller

'''Define function called "queryBuy: Implements generating results for query buy criteria for books
   Input:  "p_query" = Query from client
   Output: Returns "message", containing results of orders for books that match query buy criteria
'''
def queryBuy(p_query):
    queryAsCompentents = p_query.split()                                    #Store whitespace separated words in "p_query" in "queryAsComponent"
    queryAsCompentents.pop(0)                                               #Remove '0'-th element in "queryAsComponent", which represents query action
    
    customerName = str(queryAsCompentents[0]).capitalize()                  #Set "customerName" to '0'-th element in "queryAsComponents" 
                                                                            #(Customer name becomes '0'-th' element in "queryAsComponents" after "pop()" initial  '0'-th element defining query action
    queryAsCompentents.pop(0)                                               #Remove '0'-th' element in "queryAsComponent", which represents customer name
                                                                            #(Remaining elements represent strucutre for buy requests)
                

    buyRequests = []                                                        #Store list of buy requests for books matching criteria
    booksOrdered = []                                                       #Store list of books found in "books" matching criteria of elements in "buyRequests"


    #Populate "buyRequests" with lists containing buy parameters for buy requests provided in "queryAsCompentents"
    #NOTE: A single buy request takes two consecutive elements from "queryAsCompentents" to construct a single buy request
    #NOTE: Reference "Query Builder" at top of "server.py"
    for index in range(0, len(queryAsCompentents), 2):
        buyRequests.append(queryAsCompentents[index:index+2])

    #For each "buyRequest" in "buyRequests"
    for buyRequest in buyRequests:
        #For each "book" in "books", check if any "buyRequest" equal to "book" (i.e. Match buy request criteria)
        for book in books:
            if str(buyRequest[0]) == str(book[1]):                          #If "buyRequest" "Bk No." equal to "book" "Bk No."
                booksOrdered.append([book, buyRequest])                     #If all criteria match, store list "book" details w/ "buyRequest" list in "booksOrdered" list

    #Construct formatted return message containing books ordered matching query buy criteria
    if len(booksOrdered) > 0:                                               #If "booksOrdered" is non-empty list (i.e. Books found that match search request criteria)
        message = "\n\nThe following books were ordered:\n"                 #Set "message" to initial  header, concatenated content contains accepted order details
        altMessage = ("\nThe following books were not ordered:\n"+
                      "Reason: Reselling prevention system, "+ 
                      "Quantity exceeded: 5)\n")                            #Set "altMessage" to initial  header, concatenated content contains refused order details
                                                                            
        
        counter = 1                                                         #Counter to concatenate numerical bulletpoints to list of accepted order details                                            
        altCounter = 1                                                      #Counter to concatenate numerical bulletpoints to list of refused order details
        altMessageModified = False                                          #Only return "altMessage" content, concatenated to "message", if "True" (ie.e "altMessage" modified and set "altMessageModified to "True")
        grandTotal = 0                                                      #Store grand total of all orders
        
        #For each "bookOrdered" in "booksOrdered"
        for bookOrdered in booksOrdered:
            #If order of book less than 5, order accepted (Prevent large quantity orders for reselling)
            if int(bookOrdered[1][1]) < 5:                                  #If "bookOrdered", "orderRequest" quantity less than 5
                tempStr = (str(counter) + ") " +                            #Create "tempStr" (Temporary String) w/ numerical bulletpoint using "counter", concatenate
                           "Book Name: " +
                           str(bookOrdered[0][0]).capitalize() +            #Book name from "bookOrdered" in "booksOrdered", concatenate
                           ", Book Quantity: " +
                           str(bookOrdered[1][1]).capitalize()  +           #Book quantity from "bookOrdered" in "booksOrdered", concatenate
                           ", Sub-Total: £" +
                           str(bookOrdered[0][2]).capitalize()  +           #Book price from "bookOrdered" in "booksOrdered", concatenate
                           ", Total: £" + 
                           str(float(bookOrdered[0][2]) * 
                               int(bookOrdered[1][1])) + '\n')              #Book total price is price from "bookOrdered" multiplied by qunatity from "bookOrdered" 

                counter += 1                                                #Increment "counter" by 1
                grandTotal += (float((bookOrdered[0][2])) * 
                               int((bookOrdered[1][1])))                    #"grandTotal" = grandTotal + (Book Price in "bookOrdered" multiplied by Quantity in "bookOrdered")
                message += tempStr                                          #Concatenate "tempStr" to "message"

            #Else order of book greater than or equal to 5, order refused (Prevent large quantity orders for reselling)
            else:
                tempStr = (str(altCounter) + ") " +                         #Create "tempStr" (Temporary String) w/ numerical bulletpoint using "counter", concatenate
                           "Book Name: " + 
                           str(bookOrdered[0][0]).capitalize() +            #Book name from "bookOrdered" in "booksOrdered", concatenate
                           ", Book Quantity: " + 
                           str(bookOrdered[1][1]).capitalize()  +           #Book quantity from "bookOrdered" in "booksOrdered", concatenate
                           ", Sub-Total: £" + 
                           str(bookOrdered[0][2]).capitalize()  +           #Book price from "bookOrdered" in "booksOrdered", concatenate
                           ", Total: £" + 
                           str(float(bookOrdered[0][2]) * 
                               int(bookOrdered[1][1])) + '\n')              #Book total price is price from "bookOrdered" multiplied by qunatity from "bookOrdered" 

                altCounter += 1                                             #Increment "altCounter" by 1
                altMessage += tempStr                                       #Concatenate "tempStr" to end of "altMessage"
                altMessageModified = True                                   #Set "altMessageModified" to "True", "altMessage" modified as refused order details exist

        #Concatenate "altMessage" to "message", list of accepted order details, followed by list of refused order details
        if altMessageModified:                                              #If "altMessageModified" is "True"
            message += altMessage                                           #Concatenate "tempStr" to "altMessage"
        
        #Concatenate "customerName" and "grandTotal" to "message", deduct 10% from "grandTotal" if over £75.00 spent 
        if grandTotal > 75.00:                                              #If "grandTotal" greater then £75.00
            message += (("\nCustomer Name: " + customerName + '\n') + 
            ("Grand Total (With 10% off on purchases over £75): £" + str(round((grandTotal * 0.90), 2)) + ' ' +
             "(Savings: £" + str(round((grandTotal * 0.10), 2)) + ")\n"))   #Concatenate "customerName" to start of "message" and 10% off "grandTotal" to end of "message"
        else:
            message += (("\nCustomer Name: " + customerName + '\n') + 
            ("Grand Total: " + str(round(grandTotal, 2)) + '\n'))           #Concatenate "customerName" to start of "message" and "grandTotal" to end of "message"
        
        return message                                                      #Return "message"
    
    message = "No books matching buy criteria found\n"                    #"message" set to literal string detailing no buy requests criteria match books
    return message                                                          #Return "message"



if __name__ == '__main__':
    print("Welcome to the Nature Walk Querent (Server Module)")

    echoServer(host, port)