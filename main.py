from flask import Flask
import os
import conf

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'