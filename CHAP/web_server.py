# Dominic Cassidy 28/06/2016
# CHAP Control System

# This file creates and hosts the web server. All required web files are in
# child folder.

##############IMPORTS#################
from CHAP_Controller import app

PORT = 8080 # Port to create server on.
## Main (i.e. default method)
def start():
    
    app.debug = True
    app.run(host="",port=PORT)