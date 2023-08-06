#!/usr/bin/env python3
from pygments.formatters import HtmlFormatter
from flask import Flask, render_template, Markup, Response, g
from flask_socketio import SocketIO, emit
from multiprocessing import Process
import thebe.core.run as Run
import thebe.core.html as Html
import thebe.core.ledger as Ledger
import thebe.core.database as Database
import thebe.core.update as Update
import time, os, sys, webbrowser, argparse, logging, sqlite3, logging

#Parse commandline argument
parser = argparse.ArgumentParser(description='Display python information live in browser.')
parser.add_argument('file', metavar='F', help='python file to run')
args = parser.parse_args()
fileLocation=args.file# file to execute

#Initialize port and url
port=5000
url = 'localhost:%s' % port

#Initialize flask
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = 'secret!'
socketio= SocketIO(app)

#Configure logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

#Initialize some globals
myDir=os.path.dirname(os.path.abspath(__file__))#Absolute directory of package

'''
Set some headers and get and send css for all of the HtmlFormatter components.
'''
@app.route('/')
def home():
    css=HtmlFormatter().get_style_defs('.highlight')
    response=Response(render_template('main.html', css=css))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate" # HTTP 1.1.
    response.headers["Pragma"] = "no-cache" # HTTP 1.0.
    response.headers["Expires"] = "0" # Proxies
    return response

'''
Connect and disconnect events.
'''
@socketio.on('connect')
def connect():
    print('Connected to client')
    #Show
    Update.checkUpdate(socketio, fileLocation, connected=True)
    #Start pinging
    socketio.emit('ping client')
@socketio.on('disconnect')
def disconnect():
    print('Client disconnected')

'''
Ping back and forth from client to server.
Checks whether or not the file has been saved and running it when changed.
'''
@socketio.on('check if saved')
def check():
    print('Check if target updated...')
    Update.checkUpdate(socketio, fileLocation)
    socketio.emit('ping client')

'''
Run flask and socketio.
'''
def main():
    ledger=[]
    def startFlask():
        socketio.run(app, port=5000)#, debug=True)
#        webbrowser.open_new_tab(url)
    try:
        print('Starting flask process...')
        flask=Process(target=startFlask)
        flask.start()
    except KeyboardInterrupt:
        print("Terminating flask server.")
        flask.terminate()
        flask.join()
        print("Terminated flask server.")
