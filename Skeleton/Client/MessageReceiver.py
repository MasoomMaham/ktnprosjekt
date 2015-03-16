# -*- coding: utf-8 -*-
from threading import Thread


class MessageReceiver(Thread):
    """
    This is the message receiver class. The class inherits Thread, something that
    is necessary to make the MessageReceiver start a new thread, and permits
    the chat client to both send and receive messages at the same time
    """

    def __init__(self, client, connection):

        self.clt = client
        self.cnt = connection

        """
        This method is executed when creating a new MessageReceiver object
        """

        # Flag to run thread as a deamon
        self.daemon = True


        # TODO: Finish initialization of MessageReceiver

    def run(self):
        message = self.cnt.recv(4096)
        if message != '':
            self.clt.receive_message(message)
        pass

