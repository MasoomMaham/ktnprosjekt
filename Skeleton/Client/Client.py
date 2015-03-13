# -*- coding: utf-8 -*-
import socket
from MessageReceiver import MessageReceiver
import json


class Client:
    """
    This is the chat client class
    """

    def __init__(self, host, server_port):
        self.host = host
        self.server_port = server_port
        """
        This method is run when creating a new Client object
        """

        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.run()

        msg = MessageReceiver(self, self.connection)
    def run(self):
        # Initiate the connection to the server
        self.connection.connect((self.host, self.server_port))

    def disconnect(self):
        self.connection.close()
        pass

    def receive_message(self, message):
        temp = ''
        pass

    def send_payload(self, data):
        self.connection.send(data)
        pass
    loggedOn = False
    print("Welcome to SuperAwesome chat. Type -help if you need assistance.")
    while True:
        income = raw_input()
        print("Input: "+income)
        if income == '-help':
            helpCmd = ['The following commands are useful:'
            '\n login: type "login" followed by a return, then a line consisting only of the desired username.'
            '\n names: type only this in the console in order to retrieve all of the occupied names in the chatroom.'
            '\n logout: type only this in the console in order to log out from the server.']
            for i in helpCmd:
                print i
        elif income == '-login':
            print("Type in your desired username and you will be logged into the server as long as the username is not occupied.")
            income = raw_input()
            dataOut = 'rqst: login content: '+income
            send_payload(dataOut)






if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client('localhost', 9998)
