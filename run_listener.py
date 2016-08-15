# Dominic Cassidy 28/06/2016
# CHAP Control System

# Dynamixel comunication system. Listens on websocket for user commands.

##############IMPORTS#################
import CHAP_Controller.Dynamixel as dy
from autobahn.twisted.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory
######################################

# Variables, prepare dynamixel port
base = dy.dynamixel()
hand = dy.dynamixel()

# Locations on dynamixel registry
REG_GOAL_POSITION_L = 30
REG_GOAL_POSITION_H = 31
REG_SPEED = 32
REG_TORQUE_LIMIT = 34
REG_CURRENT_POSITION = 36

WHEEL_MODE = ([(0),(0)])
JOINT_MODE = ([(1),(1)])
KNUCKLE_SPACE = None

HAND_WRIST = 10
HAND_KNUCKLE = 11
HAND_FINGER = 12

#Wheel mode: CW/CCW = 0
#Joint mode: CW/CCW = !0
#Multi-turn mode: CW/CCW = 4095

# Web Socket class
class ServerRobotController(WebSocketServerProtocol):

    def prepareKnuckle(self):
        global KNUCKLE_SPACE
    
        torque = get_reg(HAND_KNUCKLE, ins=2, regstart=REG_TORQUE_LIMIT, rlength=1)
        SPEED = 200
        
        while(torque < 400):
            hand.set_ax_reg(HAND_KNUCKLE, REG_SPEED, ([(SPEED%256),(SPEED>>8)]))
            
        SPEED = 0
        hand.set_ax_reg(HAND_KNUCKLE, REG_SPEED, ([(SPEED%256),(SPEED>>8)]))
        
        max_position = get_reg(ID, ins=2, regstart=REG_CURRENT_POSITION, rlength=1)
        min_position = abs(max_position-2000)
        
        KNUCKLE_SPACE = [min_position,max_position]
        
    def moveKnuckle(self,targetPosition):
        global KNUCKLE_SPACE
        #Put target within range of knuckle space
        #wait until target reached

	# React to client connection, setup dynamixels.
    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))

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
        #print("Control => " + controlID + "| Value:"+str(Xvalue)+","+str(Yvalue))
        
        if controlID == "rightJoystick":
            mag, ta = dy.polar(Xvalue,Yvalue)
            v1, v2, v3 = dy.velocity(mag,ta)
            v1, v2, v3 = dy.vel_direc(v1), dy.vel_direc(v2), dy.vel_direc(v3)
            #vt = 2
            base.set_ax_reg(1, REG_SPEED, ([(v1%256),(v1>>8)]))
            base.set_ax_reg(2, REG_SPEED, ([(v2%256),(v2>>8)]))
            base.set_ax_reg(3, REG_SPEED, ([(v3%256),(v3>>8)]))
			
        elif controlID == "leftSliderHorz":
            rotation = 0
            if(xValue < 0):
                rotation = int(1024 - Xvalue)
            else:
                rotation = int(1024*Xvalue)
                
            #base.set_ax_reg(1, SPEED_REG, ([(rotation%256),(rotation>>8)]))
            #base.set_ax_reg(2, SPEED_REG, ([(rotation%256),(rotation>>8)]))
            #base.set_ax_reg(3, SPEED_REG, ([(rotation%256),(rotation>>8)]))
			
        elif controlID == "leftSliderVert":    
            v4 = 0
            if(Yvalue < 0):
                v4 = int(1023 + (1023 * (abs(Yvalue))))
                #v4 = 2000
            else:
                v4 = int(1023*Yvalue)
                #v4 = 1000
            base.set_ax_reg(4, REG_SPEED, ([(v4%256),(v4>>8)]))
            
        elif controlID == "rightPinch":    
            Xvalue
            base.set_ax_reg(HAND_KNUCKLE, REG_SPEED, ([(v4%256),(v4>>8)]))
            
    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))
        
    def __init__(self):
        super.__init__
    
        for i in range(1,4):
            base.set_ax_reg(i, REG_GOAL_POSITION_L, WHEEL_MODE)
            base.set_ax_reg(i, REG_GOAL_POSITION_H, WHEEL_MODE)
            
        #Set Wrist to Joint mode
        hand.set_ax_reg(HAND_WRIST, REG_GOAL_POSITION_L, JOINT_MODE)
        hand.set_ax_reg(HAND_WRIST, REG_GOAL_POSITION_H, JOINT_MODE)
        hand.set_ax_reg(HAND_WRIST, REG_SPEED, ([(300%256),(300>>8)]))
        
        #Set Knuckle to Wheel mode
        hand.set_ax_reg(HAND_KNUCKLE, REG_GOAL_POSITION_L, WHEEL_MODE)
        hand.set_ax_reg(HAND_KNUCKLE, REG_GOAL_POSITION_H, WHEEL_MODE)
        
        #Set Finger to Joint mode
        hand.set_ax_reg(HAND_FINGER, REG_GOAL_POSITION_L, ([(228),(950)]))
        hand.set_ax_reg(HAND_FINGER, REG_GOAL_POSITION_H, ([(228),(950)]))
        hand.set_ax_reg(HAND_FINGER, REG_SPEED, ([(150%256),(150>>8)]))
        
        prepareKnuckle()

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