import os

def get_path(dirname, filename):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", dirname, filename))
