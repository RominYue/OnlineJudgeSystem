#!/usr/bin/env python2
# -*- coding:utf-8 -*-

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
import os,sys

FLASKS_ETTINGS = '../config.py'

app = Flask(__name__)
app.config.from_pyfile(FLASKS_ETTINGS, silent = True)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/login'

print os.path.abspath(sys.path[0])


