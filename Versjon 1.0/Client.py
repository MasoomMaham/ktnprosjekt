# -*- coding: utf-8 -*-
import socket
import json
from MessageReceiver import MessageReceiver


class Client:
    """
    This is the chat client class
    """

    def __init__(self, host, server_port):
        self.hasloggedOn = False
        self.host = host
        self.server_port = server_port
        self.EarlierLogin = False
        """
        This method is run when creating a new Client object
        """

        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.msg = MessageReceiver(self, self.connection)

        self.run()

    def run(self):
        self.msg.start()
        # Initiate the connection to the server
        self.connection.connect((self.host, self.server_port))
        loggedOn = False
        print("Welcome to SuperAwesome chat. Type -help if you need assistance.")

        while True:

            income = raw_input()
            if income == '-help':
                helpCmd = ['The following commands are useful:'
                '\n -login: type "login" followed by a return, then a line consisting only of the desired username.'
                '\n -names: type only this in the console in order to retrieve all of the occupied names in the chatroom.'
                '\n -logout: type only this in the console in order to log out from the server.']
                for i in helpCmd:
                    print i
            elif income == '-login':
                print("Type in your desired username and you will be logged into the server as long as the username is not occupied.")

                income = raw_input()

                obj = {"request": "login", "content": income}
                try:
                    jsonobj = json.dumps(obj)
                except UnicodeDecodeError:
                    print("Norwegian characters are not allowed.")
                    continue
                self.send_payload(jsonobj)

                self.hasloggedOn = True

            elif income == '-logout' and self.hasloggedOn:
                print("Trying to log out.")
                obj = {"request": "logout", "content": ""}
                try:
                    jsonobj = json.dumps(obj)
                    self.send_payload(jsonobj)
                    #print("Sent logout req.")
                    #self.disconnect()
                    self.hasloggedOn = False
                except UnicodeDecodeError:
                    print("Norwegian characters are not allowed.")
                    continue

            elif income == "-logout" and not self.hasloggedOn:
                print("You have to be logged in order to log out.")

            elif income == "-names" and self.hasloggedOn:
                obj = {"request": "names", "content": ""}
                try:
                    jsonobj = json.dumps(obj)
                except UnicodeDecodeError:
                    print("Norwegian characters are not allowed.")
                    continue
                self.send_payload(jsonobj)
            elif income == "-names" and not self.hasloggedOn:
                print("You have to be logged on in order to know who is online.")
            elif income == "-history" and self.hasloggedOn:
                self.requestHistory()
            elif income == '-Quit':
                print "Bye"
                break
            elif income == '-status':
                print("Connection: "+str(self.connection))

            else:
                #if not loggedOn:
                    #print("You have to be logged on in order to chat.")
                if not self.hasloggedOn:
                    print("You have to be logged on in order to chat.")
                elif loggedOn or self.hasloggedOn:
                    obj = {"request": "msg", "content": income}
                    try:
                        jsonobj = json.dumps(obj)
                    except UnicodeDecodeError:
                        print("Norwegian characters are not allowed.")
                        continue
                    self.send_payload(jsonobj)

    def disconnect(self):
        print("Disconnecting...")
        self.connection.close()
        self.hasloggedOn = False
        self.EarlierLogin = True
        print("Loginstatus: "+str(self.hasloggedOn))
        pass

    def receive_message(self, message):

        try:
            stringmessage = message
            if type(message) == unicode:
                stringmessage = message.encode("utf-8")
            #stringmessage = str(message)
            obj = json.loads(stringmessage)
            time = obj["Timestamp"]
            sender = obj["Sender"]
            response = obj["Response"]
            body = obj["Content"]

            if response == "History" and (len(body) >= 1):
                for i in body:
                    print '[History: '+i[1]+' [Sender: '+i[0]
            elif response == "LoginFailedUserName":
                print'[Time: ' + time + ']' + '[Sender: '+sender + '[Message: '+body+' ]'
                self.hasloggedOn = False
            elif response == "History" and body == []:
                print "No history."
            elif response == "Names" and (len(body) >= 1):
                for i in body:
                    print '[ User: '+i
            elif response == "Logout":
                self.disconnect()
                print'[Time: ' + time + ']' + '[Sender: '+sender + '[Message: '+body+' ]'
            #elif response == "History" and len(body) == 0:
                #print '[Time: ' + time + ']' + '[Sender: ' + sender + ']' + ' Message: No history.'
            #else:
                #print '[Time: ' + time + ']' + '[Sender: ' + sender + ']' + ' Message: ' + body
            else:
                print '[Time: ' + time + ']' + '[Sender: ' + sender + ']' + '[Message: ' + body
            pass
        except ValueError:
            print("Not JSON.")
            print(message+" TULL")


    def send_payload(self, data):
        self.connection.send(data)
        pass

    def requestHistory(self):
        obj = {"request": "history", "content": ""}
        jsonobj = json.dumps(obj)
        self.send_payload(jsonobj)

if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client('78.91.70.217', 20000)
