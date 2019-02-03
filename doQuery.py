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
import decodeButtonPressAnswer
from constants import *

def queryGateway(slConnection):
    # send a simple query and print the response, no advanced decoding required.
    slConnection.socket.sendall(doMessages.makeMessage(code.VERSION_QUERY))
    data = slConnection.socket.recv(480)
    if not data:
      sys.stderr.write("WARNING: {}: no {} data received.\n".format(me, "VERSION_ANSWER"))
    rcvcode, data = doMessages.decodeMessage(data)
    if(rcvcode != code.VERSION_ANSWER):
      sys.stderr.write("WARNING: {}: rcvCode2({}) != {}.\n".format(me, rcvCode2, code.VERSION_ANSWER))
      sys.exit(10)
    return doMessages.getMessageString(data)

def queryConfig(slConnection):
    #get controler config
    slConnection.socket.sendall(doMessages.makeMessage(code.CTRLCONFIG_QUERY, struct.pack("<2I", 0, 0)))
    rcvcode, data = doMessages.decodeMessage(slConnection.socket.recv(1024))
    if(rcvcode != code.CTRLCONFIG_ANSWER):
      sys.stderr.write("WARNING: {}: rcvCode2({}) != {}.\n".format(me, rcvcode, code.CTRLCONFIG_ANSWER))
      sys.exit(11)
    return decodeConfigAnswer.decodeConfigAnswer(data)

def queryStatus(slConnection):
    # get pool status
    slConnection.socket.sendall(doMessages.makeMessage(code.POOLSTATUS_QUERY, struct.pack("<I", 0)))
    rcvcode, data = doMessages.decodeMessage(slConnection.socket.recv(480))
    if(rcvcode != code.POOLSTATUS_ANSWER):
      sys.stderr.write("WARNING: {}: rcvCode2({}) != {}.\n".format(me, rcvCode, code.POOLSTATUS_ANSWER))
      sys.exit(11)
    return decodeStatusAnswer.decodeStatusAnswer(data)

def queryButtonPress(slConnection, circuitID, circuitState):
    slConnection.socket.sendall(doMessages.makeMessage(code.BUTTONPRESS_QUERY, struct.pack("<III", 0, circuitID, circuitState)))
    rcvcode, data = doMessages.decodeMessage(slConnection.socket.recv(480))
    if(rcvcode != code.BUTTONPRESS_ANSWER):
      sys.stderr.write("WARNING: {}: rcvCode2({}) != {}.\n".format(me, rcvCode, code.BUTTONPRESS_ANSWER))
      sys.exit(11)
    print(rcvcode)
    return (data) #decodeButtonPressAnswer.decodeButtonPressAnswer(data)    

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
