#!/usr/bin/env python2
# -*- coding:utf-8 -*-

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

FLASKS_ETTINGS = 'config.py'

app = Flask(__name__)
app.config.from_pyfile(FLASKS_ETTINGS, silent = True)
db = SQLAlchemy(app)

from appfile import views
from models import User

