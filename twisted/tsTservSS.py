#!/usr/bin/env python

__author__ = 'horton'

"""
TCP server using SocketServer.
Modified from Core Python Application Programming, http://www.corepython.com/ .

No 3rd party libraries need to be installed to run this.

How to run these.  (Might be easier to run these from the command-line.)
a) Start the server, this  program.
b) Start the client, tsTclntSS.py, on the same computer. (In a different window.)
c) In the client, type some text input.  You'll see that it's sent to the server,
given a timestamp, and then sent back to the client, which prints the timestamped data.
d) Hit return in the client to stop the client.
e) In the server window, Hit CTRL-C or whatever your operating system requires to kill a running program.

It should be possible to run these on two different computers.
Start the server on one machine.
When you start the client on the 2nd machine, give a command-line argument: the IP address
or full internet hostname of the server machine.

"""

import SocketServer
from time import ctime
import sys

HOST = ''
# PORT = 49152
# PORT = 21567
PORT = 21568

class MyRequestHandler(SocketServer.StreamRequestHandler):
    def handle(self):
        print '...connected from:', self.client_address
        in_msg = self.rfile.readline().strip()
        print "   received from client: ", in_msg
        back_msg = '[%s] %s\n' % (ctime(), in_msg)
        self.wfile.write(back_msg)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        HOST = sys.argv[1]
    ADDR = (HOST, PORT)
    print "using (HOST,PORT): ", ADDR

    tcpSerSock = SocketServer.TCPServer(ADDR, MyRequestHandler)
    print 'waiting for connection...'
    try:
        tcpSerSock.serve_forever()
    except:
    # except KeyboardInterrupt:
        print "closing server"
        tcpSerSock.shutdown()
        tcpSerSock.server_close()