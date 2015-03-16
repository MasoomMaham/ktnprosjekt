# -*- coding: utf-8 -*-
import SocketServer
import datetime

import time
import json

class userHandler():
    connections = []
    users =[]
    global connections
    global users

    def addUser(self, user):

        users.append(user)

    def hasUser(self, user):

        for i in users:
            if i == user:
                return True
        return False
    def removeUser(self, user):

        users.remove(user)
    def getUsers(self):

        return users
    def addConnection(self, handler):

        connections.append(handler)
    def getConnections(self):

        return connections
    def removeConnection(self, conn):

        connections.remove(conn)


class ClientHandler(SocketServer.BaseRequestHandler):

    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """

    def handle(self):
        handler = userHandler()
        user = ''
        """
        This method handles the connection between a client and the server.
        """
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request

        # Loop that listens for messages from the client
        while True:
            hasLoggedIn = False
            received_string = self.connection.recv(4096)
            if received_string == '':
                received_string = self.connection.recv(4096)
                jrec = json.loads(received_string)
                body = jrec["content"]
                request = jrec["request"]
            else:
                jrec = json.loads(received_string)
                body = jrec["content"]
                request = jrec["request"]

            if request == 'login' and not hasLoggedIn:
                if handler.hasUser(body):
                    tid = time.time()
                    thisTime = datetime.datetime.fromtimestamp(tid).strftime('%H:%M:%S')
                    response = {"Timestamp": thisTime, "Sender": "Server", "Response": "Login", "Content": "The username is already in use, please choose another one."}
                    print type(response)
                    jsonresponse = json.dumps(response)
                    self.connection.send(json.dumps(jsonresponse))

                else:
                    handler.addConnection(self)
                    handler.addUser(body)
                    user = body
                    tid = time.time()
                    thisTime = datetime.datetime.fromtimestamp(tid).strftime('%H:%M:%S')
                    response = {"Timestamp": thisTime, "Sender": "Server", "Response": "Login", "Content": "Login Successful."}
                    print type(response)
                    jsonresponse = json.dumps(response)
                    self.connection.send(jsonresponse)

                    print(body+" logged in.")
            elif request == 'logout' and hasLoggedIn:
                handler.removeUser(body)
                print(body+" logged out.")
                handler.removeConnection(self)
                self.connection.close()

            elif request == 'names':
                tid = time.time()
                thisTime = datetime.datetime.fromtimestamp(tid).strftime('%H:%M:%S')
                response = {"Timestamp": thisTime, "Sender": "Server", "Response": "Names", "Content": userHandler.getUsers()}
                jsonresponse = json.dumps(response)
                self.connection.send(jsonresponse)

            elif request == 'msg':
                print("Got message: "+body)
                threads = handler.getConnections()
                print threads
                print("Number of clients: " + str(len(threads)))
                tid = time.time()
                thisTime = datetime.datetime.fromtimestamp(tid).strftime('%H:%M:%S')
                response = {"Timestamp": thisTime, "Sender": user, "Response": "Message", "Content": body}
                jsonresponse = json.dumps(response)
                for i in threads:
                    i.connection.send(jsonresponse)
                    obj = i.connection.recv(4096)
                    print obj
            #elif request == 'msg' and not hasLoggedIn:
                #print
                #tid = time.time()
                #thisTime = datetime.datetime.fromtimestamp(tid).strftime('%H:%M:%S')
                #response = {"Timestamp": thisTime, "Sender": "Server", "Response": "Error", "Content": "You have to be logged in in order to send messages,"}
                #jsonresponse = json.dumps(response)
                #self.connection.send(jsonresponse)









            
            # TODO: Add handling of received payload from client


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations is necessary
    """


    allow_reuse_address = True

if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python Server.py"
    in your terminal.

    No alterations is necessary
    """

    HOST, PORT = 'localhost', 9998
    print 'Server running...'

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
