import Dynamixel as dy
import time
hand = dy.dynamixel()

READDATA = 2
WRITE_DATA = 3

REG_GOAL_POSITION_L = 30
REG_GOAL_POSITION_H = 31
REG_SPEED = 32
REG_TORQUE_LIMIT = 34
REG_CURRENT_POSITION = 36
REG_LOAD = 40
REG_MOVING = 46

HAND_WRIST = 10
HAND_KNUCKLE = 11
HAND_FINGER = 12

WHEEL_MODE = ([(0),(0)])
JOINT_MODE = ([(1),(1)])
KNUCKLE_SPACE = None

maxPos = 0
minPos = 0

torqueLimit = 400
hand.set_ax_reg(HAND_KNUCKLE, REG_TORQUE_LIMIT, ([(torqueLimit%256),(torqueLimit>>8)]))

curLoad =  hand.get_reg(HAND_KNUCKLE, ins=READDATA, regstart=REG_LOAD, rlength=1)
print "Load: " + str(curLoad)

v1 = 1200
hand.set_ax_reg(HAND_KNUCKLE, REG_SPEED, ([(v1%256),(v1>>8)]))

while str(curLoad) != "[144]":
    curLoad =  hand.get_reg(HAND_KNUCKLE, ins=READDATA, regstart=REG_LOAD, rlength=1)
    pos =  hand.get_reg(HAND_KNUCKLE, ins=READDATA, regstart=REG_CURRENT_POSITION, rlength=1)
    print "Load: " + str(curLoad) + "Pos: " + str(pos)

maxPos = pos
    
v1 = 150
hand.set_ax_reg(HAND_KNUCKLE, REG_SPEED, ([(v1%256),(v1>>8)]))

time.sleep(3.5)

minPos =  hand.get_reg(HAND_KNUCKLE, ins=READDATA, regstart=REG_CURRENT_POSITION, rlength=1)
v1 = 0
hand.set_ax_reg(HAND_KNUCKLE, REG_SPEED, ([(v1%256),(v1>>8)]))


print "Pos: " + str(minPos) + "-" + str(maxPos)