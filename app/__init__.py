from flask import Flask

import os
import json

with open('config.json') as f:
    config = json.load(f)

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY') or config["SECRET_KEY"]

from app import routes
