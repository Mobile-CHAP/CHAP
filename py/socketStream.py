# import cv2
# import numpy as np
# import sys
# import uuid
# import os, os.path
# import shutil
from autobahn.twisted.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory

# cap = cv2.VideoCapture(0)
# imgDir = './public/stream/'

class ServerRobotVision(WebSocketServerProtocol):

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")
        self.sendMessage("goat")

    def onMessage(self, payload, isBinary):
        self.sendMessage("goat")
         
    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))


if __name__ == '__main__':

    import sys
    from twisted.python import log
    from twisted.internet import reactor

    log.startLogging(sys.stdout)

    factory = WebSocketServerFactory(u"ws://127.0.0.1:9002")
    factory.protocol = ServerRobotVision
    # factory.setProtocolOptions(maxConnections=2)

    reactor.listenTCP(9002, factory)
    reactor.run()