# -*- coding: utf-8 -*-
import SocketServer
import datetime

import time
import json

class userHandler():
    connections = []
    users = []
    history = []
    history.append(("SERVER", "ServerStart"))
    global connections
    global users
    global history

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
    def addMessage(self, message):
        history.append(message)

    def getHistory(self):
        return history


class ClientHandler(SocketServer.BaseRequestHandler):

    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """

    def handle(self):
        handler = userHandler()
        hasLoggedIn = False
        user = ''
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request
        counter = 0

        # Loop that listens for messages from the client
        while True:

            received_string = self.connection.recv(4096)
            try:
                jrec = json.loads(received_string)
                body = jrec["content"].encode()
                request = jrec["request"].encode()

                if request == 'login' and not hasLoggedIn:
                    if handler.hasUser(body):
                        print("USER EXISTS!!!")
                        tid = time.time()
                        thisTime = datetime.datetime.fromtimestamp(tid).strftime('%H:%M:%S')
                        response = {"Timestamp": thisTime, "Sender": "Server", "Response": "LoginFailedUserName", "Content": "Username occupied, please try with another one."}
                        print type(response)
                        jsonresponse = json.dumps(response)
                        self.connection.send(jsonresponse)

                    else:
                        handler.addConnection(self)
                        user = body
                        tid = time.time()
                        thisTime = datetime.datetime.fromtimestamp(tid).strftime('%H:%M:%S')
                        response = {"Timestamp": thisTime, "Sender": "Server", "Response": "Login", "Content": "Login Successful."}
                        jsonresponse = json.dumps(response)
                        self.connection.send(jsonresponse)
                        #history = handler.getHistory()
                        #response = {"Timestamp": thisTime, "Sender": "Server", "Response": "History", "Content": history }
                        #jsonresponse = json.dumps(response)
                        #recv1 = self.connection.recv(4096)
                        #self.connection.send(jsonresponse)
                        print(body+" logged in.")
                        handler.addUser(str(body))
                        hasLoggedIn = True
                        #print("CURRENT USERS: "+str(handler.getUsers()))

                elif request == 'logout':
                    print("Logged in users: "+str(handler.getUsers()))
                    print(user+" trying to log out")
                    #print handler.getConnections()
                    #handler.removeUser(str(body))
                    print("User: "+user+" should have been removed from: "+str(handler.getUsers()))
                    #print(body+" logged out.")
                    tid = time.time()
                    thisTime = datetime.datetime.fromtimestamp(tid).strftime('%H:%M:%S')
                    obj = {"Timestamp": thisTime, "Sender": "Server", "Response": "Logout", "Content": "Logout successful"}
                    jsonresponse = json.dumps(obj)
                    self.connection.send(jsonresponse)
                    handler.removeConnection(self)
                    self.connection.close()

                elif request == 'names':
                    print("Requested names.")
                    tid = time.time()
                    thisTime = datetime.datetime.fromtimestamp(tid).strftime('%H:%M:%S')
                    response = {"Timestamp": thisTime, "Sender": "Server", "Response": "Names", "Content": handler.getUsers()}
                    jsonresponse = json.dumps(response)
                    self.connection.send(jsonresponse)

                elif request == 'history':
                    print("Requested history.")
                    tid = time.time()
                    thisTime = datetime.datetime.fromtimestamp(tid).strftime('%H:%M:%S')
                    history = handler.getHistory()
                    response = {"Timestamp": thisTime, "Sender": "Server", "Response": "History", "Content": history}
                    jsonresponse = json.dumps(response)
                    self.connection.send(jsonresponse)

                elif request == 'msg' and hasLoggedIn:
                    print("Got message: "+body)
                    #tid = time.time()
                    #thisTime = datetime.datetime.fromtimestamp(tid).strftime('%H:%M:%S')
                    #obj = {"Timestamp": thisTime, "Sender": str(user), "Response": "History", "Content": str(body)}
                    #jsonresponse = json.dumps(obj)
                    hist = (user, body)
                    handler.addMessage(hist)
                    threads = handler.getConnections()
                    tid = time.time()
                    thisTime = datetime.datetime.fromtimestamp(tid).strftime('%H:%M:%S')
                    response = {"Timestamp": thisTime, "Sender": user, "Response": "Message", "Content": body}
                    jsonresponse = json.dumps(response)
                    for i in threads:
                        i.connection.send(jsonresponse)

            except ValueError:
                print("Not JSON-Object, trying again.")
                counter += 1
                if counter == 3:
                    self.connection.close()


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

    HOST, PORT = '78.91.70.217', 20000
    print 'Server running...'

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
