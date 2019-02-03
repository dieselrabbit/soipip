import gatewayLogin

class slConnection:

    def connect(self, gatewayIP, gatewayPort):
        if(gatewayIP):
            self.ip     = gatewayIP
            self.port   = gatewayPort
            self.socket = gatewayLogin.gatewayLogin(gatewayIP, gatewayPort)
            if(self.socket):
                return True
        return False

    
