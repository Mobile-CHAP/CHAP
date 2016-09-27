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
    def gen():
        while True:
            gevent.sleep(0.033)
            frame = camera.get_frame()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    # Return JPEG stream to client video feed.
    return Response(stream_with_context(gen()),mimetype='multipart/x-mixed-replace; boundary=frame')
    
def start():
    print "Stream started, port:"+ str(PORT)
    
    pool = Pool(5)
    http_server = WSGIServer(('', PORT), app,spawn=pool,log=None,error_log=None) # Create server
    http_server.serve_forever() # Host server forever