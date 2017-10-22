from bottle import template
import os

root = os.path.dirname(__file__)

def get_template(template_name, **kwargs):
    return template(get_template_path(template_name), **kwargs)

def get_template_path(template_name):
    return os.path.join(root, "views", template_name + ".tpl")
