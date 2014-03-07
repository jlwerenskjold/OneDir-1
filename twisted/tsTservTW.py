#!/usr/bin/env python

"""
TCP server using Twisted.
Modified from Core Python Application Programming, http://www.corepython.com/ .

3rd party libraries need to be installed to run this!  Use pip to install:
a) Twisted

How to run these.  (Might be easier to run these from the command-line.)
a) Start the server, this  program.
b) Start the client, tsTclntTW.py, on the same computer. (In a different window.)
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
from time import ctime

PORT = 21567

class TSServProtocol(protocol.Protocol):
    def connectionMade(self):
        clnt = self.clnt = self.transport.getPeer().host
        print '...connected from:', clnt

    def dataReceived(self, in_msg):
        print "received: ", in_msg
        out_msg = '[%s] %s' % (ctime(), in_msg)
        self.transport.write(out_msg)

if __name__ == "__main__":
    factory = protocol.Factory()
    factory.protocol = TSServProtocol
    print 'waiting for connection on PORT: ', PORT
    reactor.listenTCP(PORT, factory)
    reactor.run()