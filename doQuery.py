import socket
import doMessages
import decodeConfigAnswer
import decodeStatusAnswer
import decodeButtonPressAnswer
from constants import *

def queryGateway(gatewaySocket):
    # send a simple query and print the response, no advanced decoding required.
    gatewaySocket.sendall(doMessages.makeMessage(code.VERSION_QUERY))
    data = gatewaySocket.recv(480)
    if not data:
      sys.stderr.write("WARNING: {}: no {} data received.\n".format(me, "VERSION_ANSWER"))
    rcvcode, buff = doMessages.decodeMessage(data)
    if(rcvcode != code.VERSION_ANSWER):
      sys.stderr.write("WARNING: {}: rcvCode({}) != {}.\n".format(me, rcvCode2, code.VERSION_ANSWER))
      sys.exit(10)
    return doMessages.getMessageString(buff)

def queryConfig(gatewaySocket, data):
    #get controler config
    gatewaySocket.sendall(doMessages.makeMessage(code.CTRLCONFIG_QUERY, struct.pack("<2I", 0, 0)))
    rcvcode, buff = doMessages.decodeMessage(gatewaySocket.recv(1024))
    if(rcvcode != code.CTRLCONFIG_ANSWER):
      sys.stderr.write("WARNING: {}: rcvCode({}) != {}.\n".format(me, rcvcode, code.CTRLCONFIG_ANSWER))
      sys.exit(11)
    return decodeConfigAnswer.decodeConfigAnswer(buff, data)

def queryStatus(gatewaySocket, data):
    # get pool status
    gatewaySocket.sendall(doMessages.makeMessage(code.POOLSTATUS_QUERY, struct.pack("<I", 0)))
    rcvcode, buff = doMessages.decodeMessage(gatewaySocket.recv(480))
    if(rcvcode != code.POOLSTATUS_ANSWER):
      sys.stderr.write("WARNING: {}: rcvCode({}) != {}.\n".format(me, rcvCode, code.POOLSTATUS_ANSWER))
      sys.exit(11)
    return decodeStatusAnswer.decodeStatusAnswer(buff, data)

def queryButtonPress(gatewaySocket, circuitID, circuitState):
    gatewaySocket.sendall(doMessages.makeMessage(code.BUTTONPRESS_QUERY, struct.pack("<III", 0, circuitID, circuitState)))
    rcvcode, buff = doMessages.decodeMessage(gatewaySocket.recv(480))
    if(rcvcode != code.BUTTONPRESS_ANSWER):
      sys.stderr.write("WARNING: {}: rcvCode({}) != {}.\n".format(me, rcvCode, code.BUTTONPRESS_ANSWER))
      sys.exit(11)
    print(rcvcode)
    return True
