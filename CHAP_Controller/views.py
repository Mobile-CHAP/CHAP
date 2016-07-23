# Dominic Cassidy 28/06/2016
# CHAP Control System

# This file handles web pages, i.e. views. "route" refers to
# traditional URLs within a webpage. "/" refers to the root
# page, traditionally "index.html". This is shown on entering the web site.

##############IMPORTS#################
from CHAP_Controller import app
from camera import Camera
from flask import stream_with_context, render_template, Response, request
import gevent.monkey
######################################

# Camera object for streaming
camera = Camera()

# IP address, passed to client for web socket usage (control listener.)
serverIP = "192.168.15.22"
serverIP = "0.0.0.0"
# Show index.html, pass IP address to client.
@app.route("/", methods=['GET', 'POST'])
def root():
    return render_template("index.html", serverIPAddress=serverIP, title = 'Controller')
    

# Capture camera frames when route activated (returns image source).
@app.route('/video_feed/<cameraChoice>/')
def video_feed(cameraChoice):
    def run_camera():
        while True:
        
            # Frame rate
            # Give server enough time to listen for other requests.
            # gevent.sleep(0.017) # 60fps
            # gevent.sleep(0.02) # 50fps
            gevent.sleep(0.033) # 30fps
            # gevent.sleep(0.042)  # 24fps
            
            frame = camera.get_frame(cameraChoice) # Capture frame
            
            # Return JPEG bytes
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
    # Return JPEG stream to client video feed.
    return Response(stream_with_context(run_camera()), mimetype='multipart/x-mixed-replace; boundary=frame')
