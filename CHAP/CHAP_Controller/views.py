# Dominic Cassidy 28/06/2016
# CHAP Control System

# This file handles web pages, i.e. views. "route" refers to
# traditional URLs within a webpage. "/" refers to the root
# page, traditionally "index.html". This is shown on entering the web site.

##############IMPORTS#################
from . import app, serverIP, devMode
from flask import stream_with_context, render_template, Response, request
######################################

# IP address, passed to client for web socket usage (control listener.)
# Show index.html, pass IP address to client.
@app.route("/", methods=['GET', 'POST'])
def root():
    return render_template("index.html", serverIPAddress=serverIP,isDevMode=devMode, title = 'Controller')