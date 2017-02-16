from flask import Flask
from flask_ask import Ask, statement, question, session
import time
import json
import requests
import time
import sys
import pdb

fileLoc = '490file.txt'

app = Flask(__name__)
ask = Ask(app, "/octave")

@app.route('/')
def homepage():
    return "Storus rules"

@ask.launch
def start_skill():
    welcome_message = "Starting Pims Piano"
    return statement(welcome_message)



@ask.intent('OctaveIntent')
def change_octave(Direction):
    f = open(fileLoc, 'w+')
    f.write(Direction)
    f.close()
    closingStatement = "Changing octave " + Direction
    return statement(closingStatement)

@ask.intent('InstrumentIntent')
def change_instrument(Instrument):
    f = open(fileLoc, 'w+')
    f.write(Instrument)
    f.close()
    closingStatement = "Changing instrument to " + Instrument
    return statement(closingStatement)


@ask.session_ended
def session_ended():
    return "Piano shutting off", 200


if __name__ == '__main__':
    app.run(debug=True)