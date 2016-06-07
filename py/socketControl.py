#import Dynamixel as dy

# #test serial ports
# print mx28.port.test_ports()

from autobahn.twisted.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory


class ServerRobotController(WebSocketServerProtocol):

    #SPEED_REG = 32
    #POS_REG = 30
    #mx28 = dy.dynamixel()

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))
        #for i in range(1,4):
        #    mx28.set_ax_reg(i, 6, ([(0),(0)]))
        #    mx28.set_ax_reg(i, 8, ([(0),(0)]))

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        message = payload.decode('utf8');
        print("Text message received: {0}".format(message))
        # val = message.split(',',2)
        # Xvalue = float(val[0])
        # Yvalue = float(val[1])
        
        # mag, ta = dy.polar(Xvalue,Yvalue)
        # v1, v2, v3 = dy.velocity(mag,ta)
        # v1, v2, v3 = dy.vel_direc(v1), dy.vel_direc(v2), dy.vel_direc(v3)
        
        # mx28.set_ax_reg(1, SPEED_REG, ([(v1%256),(v1>>8)]))
        # mx28.set_ax_reg(2, SPEED_REG, ([(v2%256),(v2>>8)]))
        # mx28.set_ax_reg(3, SPEED_REG, ([(v3%256),(v3>>8)]))

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