#!/usr/bin/python

import liblo, sys, time
import socket


if len(sys.argv) < 2:
    print "You must specify a port on which to listen."
    sys.exit(1)

try:
    port = int( sys.argv[1] )
except ValueError:
    print "The parameter must be an integer."
    sys.exit(1)

# set the UDP port where
# we'll send the data
target = liblo.Address(9001)

# listen for an incoming connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", port))
s.listen(1)

try:
    # await for connections
    con, addr = s.accept()
except KeyboardInterrupt:
    print "Program terminated by the user."
    s.close()
    sys.exit(0)

while True:
    data = ""
    while len(data) < 10:
        data += con.recv( 10 - len(data) )
    print data
    (freq, mov) = data.split(" ")
    if mov == "u":
        liblo.send(target, "/oscillator-off")
    elif mov == "d":
        liblo.send(target, "/oscillator-on", float(freq))

con.close()



