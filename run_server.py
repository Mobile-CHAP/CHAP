# Dominic Cassidy 28/06/2016
# CHAP Control System

# This file creates and hosts the web server. All required web files are in
# child folder.

##############IMPORTS#################
from CHAP_Controller import app

import gevent.monkey
from gevent.wsgi import WSGIServer
from gevent.pool import Pool
######################################

gevent.monkey.patch_all() # Fix to ensure multiple clients possible.

serverIP = "192.168.15.22" # Used for printing IP, ignore.
PORT = 80 # Port to create server on. Will be 80 in future.

##Run Server
def run_server():
    print "Server started " + str(serverIP)+ ":" + str(PORT)
	
    pool = Pool(5) # Limit server to 5 clients.
    app.debug = True
    http_server = WSGIServer(('', PORT), app,spawn=pool,log=None,error_log=None) # Create server
    http_server.serve_forever() # Host server forever
    
## Main (i.e. default method)
if __name__ == "__main__":
    run_server()