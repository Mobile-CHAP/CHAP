from flask import Flask, stream_with_context, render_template, Response
from camera import Camera

import gevent.monkey
from gevent.wsgi import WSGIServer
from gevent.pool import Pool

gevent.monkey.patch_all()
app = Flask(__name__, static_url_path='/static')
camera = Camera()

@app.route("/")
def root():
    return render_template("index.html", title = 'Controller')

@app.route('/video_feed')
def video_feed():
    def run_camera():
        while True:
            # Give server enough time to listen for other requests.
            #gevent.sleep(0.017) # 60fps
            #gevent.sleep(0.02) # 50fps
            gevent.sleep(0.033) # 30fps
            #gevent.sleep(0.042)  # 24fps
            frame = camera.get_frame()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    return Response(stream_with_context(run_camera()), mimetype='multipart/x-mixed-replace; boundary=frame')

def run_server():
    print "Server running on port 8080"
    pool = Pool(5)
    http_server = WSGIServer(('', 8080), app,spawn=pool)
    http_server.serve_forever()
    
if __name__ == "__main__":
    run_server()