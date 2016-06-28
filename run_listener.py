# Dominic Cassidy 28/06/2016
# CHAP Control System

# Dynamixel comunication system. Listens on websocket for user commands.

##############IMPORTS#################
import CHAP_Controller.Dynamixel as dy
from autobahn.twisted.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory
######################################

# Variables, prepare dynamixel port
mx28 = dy.dynamixel()
SPEED_REG = 32 # Location on dynamixel registry for speed controller.
POS_REG = 30 # Location on dynamixel registry for position controller.

# Web Socket class
class ServerRobotController(WebSocketServerProtocol):

	# React to client connection, setup dynamixels.
    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))
        for i in range(1,4):
            mx28.set_ax_reg(i, 6, ([(0),(0)]))
            mx28.set_ax_reg(i, 8, ([(0),(0)]))

	# Socket ready for messages
    def onOpen(self):
        print("WebSocket connection open.")

	# Recieve message from client
    def onMessage(self, payload, isBinary):
        message = payload.decode('utf8');
        #print("Text message received: {0}".format(message))

        val = message.split(',',3)
        controlID = val[0]
        Xvalue = float(val[1])
        Yvalue = float(val[2])
        print("Control => " + controlID + "| Value:"+str(Xvalue)+","+str(Yvalue))
        
        if controlID == "rightJoystick":
            mag, ta = dy.polar(Xvalue,Yvalue)
            v1, v2, v3 = dy.velocity(mag,ta)
            v1, v2, v3 = dy.vel_direc(v1), dy.vel_direc(v2), dy.vel_direc(v3)
            #vt = 2
            mx28.set_ax_reg(1, SPEED_REG, ([(v1%256),(v1>>8)]))
            mx28.set_ax_reg(2, SPEED_REG, ([(v2%256),(v2>>8)]))
            mx28.set_ax_reg(3, SPEED_REG, ([(v3%256),(v3>>8)]))
			
        elif controlID == "leftSliderHorz":
            rotation = 0
            #if(xValue < 0):
            #    rotation = int(1024 - Xvalue)
            #else:
            #    rotation = int(1024*Xvalue)
                
            #mx28.set_ax_reg(1, SPEED_REG, ([(rotation%256),(rotation>>8)]))
            #mx28.set_ax_reg(2, SPEED_REG, ([(rotation%256),(rotation>>8)]))
            #mx28.set_ax_reg(3, SPEED_REG, ([(rotation%256),(rotation>>8)]))
			
        elif controlID == "leftSliderVert":    
            v4 = 0
            if(Yvalue < 0):
                v4 = int(1023 + (1023 * (abs(Yvalue))))
                #v4 = 2000
            else:
                v4 = int(1023*Yvalue)
                #v4 = 1000
            mx28.set_ax_reg(4, SPEED_REG, ([(v4%256),(v4>>8)]))
            
    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))


if __name__ == '__main__':

    import sys

    from twisted.python import log
    from twisted.internet import reactor

    log.startLogging(sys.stdout)

    factory = WebSocketServerFactory(u"ws://127.0.0.1:9001")
    factory.protocol = ServerRobotController
    # factory.setProtocolOptions(maxConnections=2)

    reactor.listenTCP(9001, factory)
    reactor.run()