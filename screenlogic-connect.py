#! /usr/bin/env python
# -*- coding: UTF8 -*-
# copyright 2018, Keith P Jolley, keithpjolley@gmail.com, squalor heights, ca, usa
# Thu May 31 16:47:03 PDT 2018

# puts everything together. broadcasts for a gateway and then queries it.

import discoverGateway
import gatewayLogin
import doQuery
import socket
from constants import me

if __name__ == "__main__":
  verbose = True
  gatewayIP, gatewayPort, gatewayType, gatewaySubtype, gatewayName, okchk = discoverGateway.discoverGateway(verbose)
  if(gatewayIP):
    tcpSock = gatewayLogin.gatewayLogin(gatewayIP, gatewayPort)
    doQuery.queryGateway(tcpSock)
    tcpSock.close()
  else:
    print("INFO: {}: could not find a gateway on this subnet.".format(me()))
