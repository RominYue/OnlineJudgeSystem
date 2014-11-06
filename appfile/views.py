#!/usr/bin/env python2
# -*- coding:utf-8 -*-

from appfile import app

import flask

@app.route('/')
@app.route('/index')
def index():
    return flask.render_template('index.html')

@app.route('/login')
def login():
    return flask.render_template('login.html')

@app.route('/register')
def register():
    return flask.render_template('register.html')
