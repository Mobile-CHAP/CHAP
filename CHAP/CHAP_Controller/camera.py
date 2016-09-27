"""
Camera class defined for use by video stream.
"""
import numpy as np
import cv2

class Camera():
    """
    Class for accessing USB camera using OpenCV.
    """
    def __init__(self):
        """
        Initialise camera object. Get VideoCapture object from camera 0.

        @rtype:   Camera
        @return:  Camera object.
        """
        self.cap = cv2.VideoCapture(0)
        
    def __del__(self):
        """
        Camera object deleted. Release camera.
        """
        self.cap.release()

    def get_frame(self):
        """
        Get current frame. Encode frame to JPEG and return bytes.
        
        @rtype:   Bytes
        @return:  JPEG encoded frame as Bytes.
        """
        ret, frame = self.cap.read()
        suc, jpeg = cv2.imencode(".jpg",frame)

        return jpeg.tobytes()