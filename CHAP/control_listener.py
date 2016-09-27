# Dominic Cassidy 28/06/2016
# CHAP Control System

# Dynamixel comunication system. Listens on websocket for user commands.

##############IMPORTS#################
import platform
import os, yaml
import pypot.dynamixel
if "ARM" in platform.uname()[4]:
    import RPi.GPIO as GPIO
else:
    GPIO = 0
import CHAP_Controller.Dynamixel as dy
from autobahn.twisted.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory
######################################

settingsPath = os.path.join(os.getcwd()) 
settings = yaml.safe_load(open(settingsPath + "\settings.yml"))

# Base Variables
wheels_one = settings['dynamixel']['wheels'][0]
wheels_two = settings['dynamixel']['wheels'][1]
wheels_three = settings['dynamixel']['wheels'][2]
base_tower = settings['dynamixel']['base']

# Gripper Variables
gripper_wrist = settings['dynamixel']['gripper']['wrist']
gripper_knuckle = settings['dynamixel']['gripper']['knuckle']
gripper_finger = settings['dynamixel']['gripper']['finger']

gripper_wrist_min = -160
gripper_wrist_max = 90

gripper_finger_min = -120
gripper_finger_max = 160

#Dynamixel Setup
baseIDs = (base_tower,wheels_one,wheels_two,wheels_three)
gripperIDs = (gripper_wrist,gripper_knuckle,gripper_finger)

#Connect to Dynamixels
gripper_port = None
base_port = None

base_wheel_mode = (base_tower,wheels_one,wheels_two,wheels_three)
hand_joint_mode = (gripper_wrist,gripper_finger)
hand_wheel_mode = (gripper_knuckle,)

if settings['devMode'] == False:
    while gripper_port is None:
        try:
            gripper_port = pypot.dynamixel.find_port(gripperIDs)
        except IndexError, e:
            print "Failed to connect to gripper dynamixel, retrying..."
            
    while base_port is None:
        try:
            base_port = pypot.dynamixel.find_port(baseIDs)
        except IndexError, e:
            print "Failed to connect to base dynamixel, retrying..."

    #Prepare Base
    base_io = pypot.dynamixel.DxlIO(base_port,timeout=2)
    base_io.enable_torque(base_wheel_mode)
    base_io.set_wheel_mode(base_wheel_mode)
        
    #Prepare Gripper
    hand_io = pypot.dynamixel.DxlIO(gripper_port,timeout=2)
    hand_io.set_joint_mode(hand_joint_mode)
    hand_io.set_wheel_mode(hand_wheel_mode)
    hand_io.enable_torque(hand_wheel_mode)
    hand_io.set_max_torque({gripper_knuckle:400})
    hand_io.set_torque_limit({gripper_knuckle:400})

    hand_io.set_moving_speed({gripper_wrist:200})
    hand_io.set_moving_speed({gripper_finger:200})
    hand_io.set_angle_limit({gripper_wrist:(gripper_wrist_min,gripper_wrist_max)})
    hand_io.set_angle_limit({gripper_finger:(gripper_finger_min,gripper_finger_max)})

    #Reset Positions
    hand_io.set_goal_position({gripper_wrist:gripper_wrist_min})
    hand_io.set_goal_position({gripper_finger:gripper_finger_min})

class IOBumper():
    def __init__(self,ioPin,powerPin):
        """
        Setup Bumper GPIO pins.
        BCM number is expected (i.e. ID, not position on board).

        @type  ioPin: number
        @param ioPin: Input/Ouput pin on Rasperry Pi used.
        
        @type  powerPin: number
        @param powerPin: Pin used to supply power to gate. Any GPIO capable of 3.3V (all standard GPIO on Pi). 
        
        @rtype:   IOBumper
        @return:  IOBumper object.
        """
        self.ioPin = ioPin
    
        GPIO.setup(ioPin,GPIO.IN)
        GPIO.setup(powerPin,GPIO.OUT)
        
        GPIO.output(powerPin,GPIO.HIGH)
        
    def read(self):
        """
        Return current value of GPIO pin. This corresponds to gate positions.
        
        @rtype:   number
        @return:  0 = open. 1 = closed.
        """
        return GPIO.input(self.ioPin)

if GPIO != 0:
    GPIO.setmode(GPIO.BCM)
    topBumper = IOBumper(ioPin=27,powerPin=5)
    botBumper = IOBumper(ioPin=13,powerPin=26)
    
    print "GPIO only usable on Raspberry Pi"

# Web Socket class
class ServerRobotController(WebSocketServerProtocol):

    def onConnect(self, request):
        """
        React to client connection.
        """
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        """
        Socket ready to recieve messages. The client waits until this point before sending messages.
        """
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        """
        Recieve message from client
        """
        message = payload.decode('utf8');
        
        if "[ERROR]//" in message:
            print message
            return

        if "[BODY]" in message:
            val = message.split(',',3)
            controlID = val[0]
            Xvalue = float(val[1])
            Yvalue = float(val[2])
            print("[CONTROL]//"+ controlID + ","+str(Xvalue)+","+str(Yvalue))
            
            if controlID == "[BODY]rightJoystick":
                mag, ta = dy.polar(Xvalue,Yvalue)
                v1, v2, v3 = dy.velocity(mag,ta)
                
                #print "[VELOCITY]// 1:%s 2:%s 3:%s" % (v1,v2,v3)

                base_io.set_moving_speed({wheels_one:v1})
                base_io.set_moving_speed({wheels_two:v2})
                base_io.set_moving_speed({wheels_three:v3})
                
            elif controlID == "[BODY]leftSliderHorz":
                rotation = 500 * Xvalue
                base_io.set_moving_speed({wheels_one:rotation})
                base_io.set_moving_speed({wheels_two:rotation})
                base_io.set_moving_speed({wheels_three:rotation})
                
            elif controlID == "[BODY]leftSliderVert":    
                #Up/Down
                v4 = 0
                if Yvalue < 0: #Going up
                    if topBumper.read() == 1:
                        v4 = 1000 * Yvalue
                    else:
                        print "Reached top"
                else: #Going down
                    if botBumper.read() == 1:
                        v4 = 1000 * Yvalue
                    else:
                        print "Reached bottom"
                
                base_io.set_moving_speed({base_tower:v4})
        
        if "[HAND]" in message:
            val = message.split(',',2)
            controlID = val[0]
            Yvalue = float(val[1])
            print("[CONTROL]//"+ controlID + ","+str(Yvalue))
             
            if controlID == "[HAND]gripper_wrist":
            
                tempGoal = (abs(gripper_wrist_min)+abs(gripper_wrist_max))*Yvalue
                goal = gripper_wrist_max - tempGoal
            
                hand_io.set_goal_position({gripper_wrist:goal})
                
            elif controlID == "[HAND]gripper_knuckle":
                speed = Yvalue*200
            
                hand_io.set_moving_speed({gripper_knuckle:speed})
            
            elif controlID == "[HAND]gripper_finger":
                tempGoal = (abs(gripper_finger_min)+abs(gripper_finger_max))*Yvalue
                goal = gripper_finger_max - tempGoal
            
                hand_io.set_goal_position({gripper_finger:goal})
        
            
    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))
        base_io.set_moving_speed({wheels_one:0})
        base_io.set_moving_speed({wheels_two:0})
        base_io.set_moving_speed({wheels_three:0})
        
    def __init__(self):
        WebSocketServerProtocol.__init__(self)
    
        #for i in range(1,4):
        #    base.set_ax_reg(i, REG_GOAL_POSITION_L, WHEEL_MODE)
        #    base.set_ax_reg(i, REG_GOAL_POSITION_H, WHEEL_MODE)
            
    def __del__(self):
        GPIO.cleanup()
        print "Cleanup up Pi GPIO"
        
        base_io.set_moving_speed({wheels_one:0})
        base_io.set_moving_speed({wheels_two:0})
        base_io.set_moving_speed({wheels_three:0})
        print "Cleanup up Dynamixel"
        
        print "Server terminated...Have a nice day."


def start():
    from twisted.python import log
    from twisted.python.logfile import DailyLogFile
    from twisted.internet import reactor

    if settings['devMode'] == False:     
        #Setup WebSocket
        log.startLogging(DailyLogFile.fromFullPath(settings['release']['log']))

        factory = WebSocketServerFactory(u"ws://127.0.0.1:9001")
        factory.protocol = ServerRobotController

        reactor.listenTCP(9001, factory)
        reactor.run()