#!/env/python
#coding=utf-8

import asyncore, socket

class Server(asyncore.dispatcher):
    """Server side for group chat

    We just override handle_accept() here to arrange client connections.
    You can override or add method if necessary, the same as other subclass of 
    dispatcher. For each connection, we initiate an instance of the EchoHandler, 
    subclass of asyncore.dispatcher, to deal with it
    """

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind((host, port))
        # limit connections to 5
        self.listen(5)
        # we create a list of clients and we need to maintain it when working
        self.clients = []

    def handle_accept(self):
        """when we receive a client connection we initiate an instance 
        of EchoHandler
        """
        socket, address = self.accept()
        print 'Connection by', address
        self.clients.append(EchoHandler(self, socket))
        message = 'Broadcast: Welcome %s' % repr(address)
        print message
        self.broadcast(message)

    def broadcast(self, message, client=None):
        """broadcast messages to everybody in client list except the client 
        passed in
        """
        if not len(message):
            return
        for c in [x for x in self.clients if x is not client]:
            c.add_message(message)


class EchoHandler(asyncore.dispatcher):
    """Handler class for each socket connection
    """

    def __init__(self, server, socket):
        asyncore.dispatcher.__init__(self, socket)
        self.server = server
        # build a buffer to capture messages
        self.buffer = ''

    def writable(self):
        """return True if you need to call handle_write when write to socket
        """
        return len(self.buffer) > 0

    def readable(self):
        """much like the above function, returning True is recommended
        we are always happy to read from client
        """
        return True

    def add_message(self, message):
        self.buffer += message

    def handle_read(self):
        """called when get messages from socket and get True from 
        self.readable()
        """
        data = self.recv(1024)
        if not data:
            pass
        else:
            message = '{0} {1}'.format(self.addr, data)
            print 'Receive from', message
            self.server.broadcast(message, self)

    def handle_write(self):
        """called when get True from self.writable()
        """
        if self.buffer:
            print 'sent', self.buffer
            sent = self.send(self.buffer)
            self.buffer = self.buffer[sent:]

    def handle_close(self):
        """called when client close socket connection
        """
        print 'Connection close', self.addr
        self.close()
        message = 'Broadcast: %s left' % repr(self.addr)
        self.server.broadcast(message, self)
        # need to remove client from list
        self.server.clients.remove(self)

s = Server('127.0.0.1', 5007)
asyncore.loop()