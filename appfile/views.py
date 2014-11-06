#!/usr/bin/env python2
# -*- coding:utf-8 -*-

from appfile import app

import flask

@app.route('/')
def index():
    return 'hello world!'
