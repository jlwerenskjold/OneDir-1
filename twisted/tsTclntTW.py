#!/usr/bin/env python

"""
TCP client using Twisted.
Modified from Core Python Application Programming, http://www.corepython.com/ .

3rd party libraries need to be installed to run this!  Use pip to install:
a) Twisted

How to run these.  (Might be easier to run these from the command-line.)
a) Start the server, tsTservTW.py.
b) Start the client, this program, on the same computer. (In a different window.)
c) In the client, type some text input.  You'll see that it's sent to the server,
given a timestamp, and then sent back to the client, which prints the timestamped data.
d) Hit return in the client to stop the client.
e) In the server window, Hit CTRL-C or whatever your operating system requires to kill a running program.

It should be possible to run these on two different computers.
Start the server on one machine.
When you start the client on the 2nd machine, give a command-line argument: the IP address
or full internet hostname of the server machine.

"""

from twisted.internet import protocol, reactor
import sys

HOST = '127.0.0.1'
# HOST = '128.143.69.241'
PORT = 21567

class TSClntProtocol(protocol.Protocol):
    def sendData(self):
        """
        Our own method, does NOT override anything in base class.
        Get data from keyboard and send to the server.
        """
        data = raw_input('> ')
        if data:
            self.transport.write(data)
        else:
            self.transport.loseConnection() # if no data input, close connection

    def connectionMade(self):
        """ what we'll do when connection first made """
        self.sendData()

    def dataReceived(self, data):
        """ what we'll do when our client receives data """
        print "client received: ", data
        self.sendData()  # let's repeat: get more data to send to server

class TSClntFactory(protocol.ClientFactory):
    protocol = TSClntProtocol
    # next, set methods to be called when connection lost or fails
    clientConnectionLost = clientConnectionFailed = \
        lambda self, connector, reason: reactor.stop()  # version from book
        # lambda self, connector, reason: handleLostFailed(reason)

# Heck, I had this working with the code just above this, so you didn't need
# the lamba.  But then I broke it.  Will post a new version with a fix.
def handleLostFailed1(reason):
    print 'Connection closed, lost or failed.  Reason:', reason
    reactor.stop()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        HOST = sys.argv[1]
    print "Connecting to (HOST, PORT): ", (HOST, PORT)
    reactor.connectTCP(HOST, PORT, TSClntFactory())
    reactor.run()
