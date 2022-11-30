import json, os
from __init__ import app


def read_json(path):
    with open(path,'r') as f:
        data = json.load(f)

    return data

def load_books():
    return read_json(os.path.join(app.root_path, 'data/Books.json'))