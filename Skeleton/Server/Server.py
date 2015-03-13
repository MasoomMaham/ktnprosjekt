# -*- coding: utf-8 -*-
import SocketServer
import sys
sys.path.append(0,'Skeleton/Client/')
import time

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






class ClientHandler(SocketServer.BaseRequestHandler):
    server = userHandler()
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
            received_string_list = received_string.split()
            if received_string == '':
                print("Print something" + received_string)
                received_string = self.connection.recv(4096)
                received_string_list = received_string.split()
                print received_string
            elif received_string_list[0] == 'rqst:':
                if received_string_list[1] == 'login' and not hasLoggedIn:
                    if userHandler.hasUser(received_string_list[3]):
                        self.connection.send('This username is in use. Choose another one.')
                    else:
                        userHandler.addUser(received_string_list[1])
                        user = received_string_list[1]
                        response = 'response: Login successful'
                        self.connection.send(response)
                        hasLoggedIn = True

                elif received_string_list[1] == 'logout':
                    self.connection.close()
                    userHandler.removeUser(user)
                elif received_string_list[1] == 'names':
                    usrs = userHandler.getUsers()
                    outString = ''
                    for i in usrs:
                        outString += i + '\n'
                    self.connection.send(outString)
                elif received_string_list[1] == 'help':
                    self.connection.send(userHandler.printHelp())



            elif input == 'Quit':
                global server
                server.exit()
            else:
                self.connection.send('Invalid input, type help for commands.')







            
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
