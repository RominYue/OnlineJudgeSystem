#!/usr/bin/env python2
# -*- coding:utf-8 -*-

from flask import Flask

FLASKS_ETTINGS = 'config.py'

app = Flask(__name__)
app.config.from_pyfile(FLASKS_ETTINGS, silent = True)

from appfile import views

