import cv2
import numpy as np

class Camera(object):
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
    
    def __del__(self):
        self.cap.release()

    def get_frame(self):
        suc, frame = self.cap.read()
        ret, jpeg = cv2.imencode(".jpg",frame)
        return jpeg.tobytes()