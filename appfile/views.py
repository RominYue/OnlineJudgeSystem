#!/usr/bin/env python2
# -*- coding:utf-8 -*-

from appfile import app

from flask import render_template,request,g
from forms import RegisterForm
from config import USERID_ERROR, NICKNAME_ERROR, PASSWORD_ERROR, EQUAL_ERROR

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm()
    if request.method == 'GET':
        return render_template('register.html',form=form)
    else:
        if not form.validate_userID():
            error = USERID_ERROR
        elif not form.validate_nickname():
            error = NICKNAME_ERROR
        elif not form.validate_password():
            error = PASSWORD_ERROR
        elif not form.validate_equal():
            error = EQUAL_ERROR
        else:
            error = None

        if error:
            return render_template('register.html',form=form, error=error)
        else:
            return render_template('index.html')

@app.route('/problemset')
def problemset():
    return render_template('base.html')
