import os

root = os.path.dirname(__file__)

def get_template_path(template_path):
    return os.path.join(root, "views", template_path + ".tpl")
