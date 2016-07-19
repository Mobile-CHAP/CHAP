import cv2
import numpy as np

class Camera(object):
    def __init__(self):
        self.cap = (cv2.VideoCapture(0),cv2.VideoCapture(1))
        
        for c in self.cap:
            c.set(3,720)
            c.set(4,576)

        
    def __del__(self):
        for c in self.cap:
            c.release()

    def get_frame(self,camera="left"):
    
        if camera == "right":
            suc, frame = self.cap[1].read()
        else:
            suc, frame = self.cap[0].read()
            
        ret, jpeg = cv2.imencode(".jpg",frame)
        return jpeg.tobytes()