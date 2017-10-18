from bottle import get, run, template, static_file

@get('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

@get('<path:path>')
def static(path):
    return static_file(path, root=".")

run(host='localhost', port=8888)
