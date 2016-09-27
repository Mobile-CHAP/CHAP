# Dominic Cassidy 28/06/2016
# CHAP Control System

# Used to link views, i.e. web pages, to main application.
import yaml
import os.path
from flask import Flask

# Flask web app.
app = Flask(__name__)

# IP address, passed to client for web socket usage (control listener.)
settingsPath = os.path.join(os.getcwd()) 
settings = yaml.safe_load(open(settingsPath + "\settings.yml"))

devMode = settings['devMode']
serverIP = settings['dev']['serverIP']

print "Server accessible at: ",serverIP+":8080"
if devMode:
    print "Running in development mode. Websockets disabled."

from . import views