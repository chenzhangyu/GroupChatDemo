#!/env/python
#coding=utf-8

import asyncore, socket
import threading

class Client(asyncore.dispatcher):
    """Client side for group chat

    To continually get input message from stand input, we use threading 
    below."""


    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))
        self.buffer = ''

    def writable(self):
        return False

    def readable(self):
        return True

    def handle_read(self):
        data = self.recv(1024)
        if data:
            print 'Received', data
        else:
            self.close()
            print '\nServer closed!'

    def handle_write(self):
        pass

c = Client('127.0.0.1', 5007)
loop_thread = threading.Thread(target=asyncore.loop)
loop_thread.daemon = True
loop_thread.start()
try:
    while 1:
        message = raw_input()
        c.send(message.strip())
except KeyboardInterrupt:
   c.close() 
finally:
   print '\n', 'Connection closed!'