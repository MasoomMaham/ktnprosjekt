# -*- coding: utf-8 -*-
import SocketServer
import sys

import time
import json

class userHandler():
    users = []
    connections = []

    def addUser(self, user):
        global users
        users.append(user)

    def hasUser(self, user):
        global users
        for i in users:
            if users[i] == user:
                return True
        return False
    def removeUser(self, user):
        global users
        users.remove(user)
    def getUsers(self):
        global users
        return users
    def printHelp(self):
        global helpCmd
        outString = ''
        for i in helpCmd:
            outString += i
        return outString
    def addConnection(self, handler):
        global connections
        connections.append(handler)
    def getConnections(self):
        global connections
        return connections
    def removeConnection(self, conn):
        global connections
        connections.remove(conn)


class ClientHandler(SocketServer.BaseRequestHandler):
    handler = userHandler()
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """

    def handle(self):
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
                print("Print something" + received_string)
            elif received_string[0] != '{':
                received_string = self.connection.recv(4096)
            else:
                print received_string
                jrec = json.loads(received_string)
                body = jrec["content"]
                request = jrec["request"]
                print body
                print request

            if request == 'login' and not hasLoggedIn:
                if userHandler.hasUser(body):
                    response = u'{"Timestamp": time.localtime(), "Sender": "Server", "Response": "Login", "Content": "The username is already in use, please choose another one."}'
                    self.connection.send(json.dumps(response))
                else:
                    userHandler.addConnection(self.connection)
                    userHandler.addUser(body)
                    response = u'{"Timestamp": time.localtime(), "Sender": "Server", "Response": "Login", "Content": "Login Successful."}'
                    self.connection.send(json.dumps(response))
            elif request == 'logout' and hasLoggedIn:
                userHandler.removeUser(body)
                userHandler.removeConnection(self.connection)
                self.connection.close()

            elif request == 'names':









            
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
