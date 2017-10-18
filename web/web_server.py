import os
from bottle import get, run, template, static_file
from board import Board

@get('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

@get('<path:path>')
def static(path):
    return static_file(path, root=os.path.dirname(__file__))

run(host='localhost', port=8888)
