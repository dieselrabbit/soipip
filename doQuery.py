#! /usr/bin/env python
# -*- coding: UTF8 -*-

# doQuery.py
# copyright 2018, Keith P Jolley, keithpjolley@gmail.com, squalor heights, ca, usa
# Thu May 31 16:47:03 PDT 2018

# sends the gateway a few commands and decodes/prints the responses.

import socket
import gatewayLogin
import doMessages
import decodeConfigAnswer
import decodeStatusAnswer
from constants import *

def queryGateway(tcpSock):
    # send a simple query and print the response, no advanced decoding required.
    tcpSock.sendall(doMessages.makeMessage(code.VERSION_QUERY))
    data = tcpSock.recv(480)
    if not data:
      sys.stderr.write("WARNING: {}: no {} data received.\n".format(me, "VERSION_ANSWER"))
    rcvcode, data = doMessages.decodeMessage(data)
    if(rcvcode != code.VERSION_ANSWER):
      sys.stderr.write("WARNING: {}: rcvCode2({}) != {}.\n".format(me, rcvCode2, code.VERSION_ANSWER))
      sys.exit(10)
    print(doMessages.getMessageString(data))

    #get controler config
    tcpSock.sendall(doMessages.makeMessage(code.CTRLCONFIG_QUERY, struct.pack("<2I", 0, 0)))
    rcvcode, data = doMessages.decodeMessage(tcpSock.recv(1024))
    if(rcvcode != code.CTRLCONFIG_ANSWER):
      sys.stderr.write("WARNING: {}: rcvCode2({}) != {}.\n".format(me, rcvcode, code.CTRLCONFIG_ANSWER))
      sys.exit(11)
    print(decodeConfigAnswer.decodeConfigAnswer(data))

    # send a more advanced query and print the response. decoding done in "decodeStatusAnswer.py"
    tcpSock.sendall(doMessages.makeMessage(code.POOLSTATUS_QUERY, struct.pack("<I", 0)))
    rcvcode, data = doMessages.decodeMessage(tcpSock.recv(480))
    if(rcvcode != code.POOLSTATUS_ANSWER):
      sys.stderr.write("WARNING: {}: rcvCode2({}) != {}.\n".format(me, rcvCode2, code.POOLSTATUS_ANSWER))
      sys.exit(11)
    print(decodeStatusAnswer.decodeStatusAnswer(data))

# same as "screen-logic.py" but you supply the host and port
if __name__ == "__main__":
  import sys
  if(len(sys.argv) != 3):
    print("ERROR: {}: usage: '{} gatewayIP port'".format(me(), me()))
    sys.exit(20)
  # don't bother checking for saneness, our user is really smart
  gatewayIP = sys.argv[1]
  gatewayPort = sys.argv[2]
  tcpSock = gatewayLogin(gatewayIP, gatewayPort)
  queryGateway(tcpSock)
