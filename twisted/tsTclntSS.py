#!/usr/bin/env python

__author__ = 'horton'

"""
TCP client using SocketServer.
Modified from Core Python Application Programming, http://www.corepython.com/ .

No 3rd party libraries need to be installed to run this.

How to run these.  (Might be easier to run these from the command-line.)
a) Start the server, tsTservSS.py.
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

from socket import *
import sys

HOST = '127.0.0.1'
# PORT = 49152 # 21567
PORT = 21568
BUFSIZ = 1024
ADDR = (HOST, PORT)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        HOST = sys.argv[1]
    print "using (HOST,PORT): ", (HOST,PORT)

    while True:
        tcpCliSock = socket(AF_INET, SOCK_STREAM)
        tcpCliSock.connect(ADDR)
        # get input from keyboard
        data = raw_input('> ')
        if not data:
            break
        tcpCliSock.send(data+'\n')

        # get response from server
        data = tcpCliSock.recv(BUFSIZ)
        if not data:
            break
        print "received from server: ", data.strip()
        tcpCliSock.close()