from CHAP_Controller.camera import Camera
from flask import Flask, Response, stream_with_context
from threading import Thread
from gevent.pywsgi import WSGIServer
from gevent.pool import Pool
import gevent.monkey

gevent.monkey.patch_all() 

app = Flask(__name__)
app.debug = False

PORT = 8081
camera = Camera()
               
# Capture camera frames when route activated (returns image source).
@app.route('/video_feed/')
def video_feed():
    """
    Handles continous return of current camera frame as part of a multpart HTTP response.
    
    - **return**::

          :return: HTTP Response containing Multitype image byte.
    """
    def gen():
        """
        Actual image capture loop. Captures frame every 0.033 seconds.
        Wait is emplacement to avoid freezing thread and not allowing new clients to connect.
        
        - **return**::

              :return: JPEG fram bytes
        """
        while True:
            gevent.sleep(0.033)
            frame = camera.get_frame()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    # Return JPEG stream to client video feed.
    return Response(stream_with_context(gen()),mimetype='multipart/x-mixed-replace; boundary=frame')
    
def start():
    """
    This function is used by CHAP main to start the server following user console command.
    """
    print "Stream started, port:"+ str(PORT)
    
    pool = Pool(5)
    http_server = WSGIServer(('', PORT), app,spawn=pool,log=None,error_log=None) # Create server
    http_server.serve_forever() # Host server forever