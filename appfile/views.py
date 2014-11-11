#!/usr/bin/env python2
# -*- coding:utf-8 -*-

from appfile import app, login_manager

from flask import render_template,request,g, redirect, url_for
from flask.ext.login import login_user, logout_user, login_required, current_user
from forms import RegisterForm, LoginForm, ProblemForm
from config import USERID_ERROR, NICKNAME_ERROR, PASSWORD_ERROR, EQUAL_ERROR, CHECK_USERID_ERROR, CHECK_PASSWORD_ERROR, EXIST_ERROR, PERMISSION_ERROR, INPUT_ERROR, UPLOAD_SUCESS
from models import User, Problem
from functools import wraps
import os

def admin_required(func):
    @wraps(func)
    def check():
        if current_user.is_authenticated() and current_user.is_admin:
            return func()
        else:
            return PERMISSION_ERROR

    return check


#userid just a parameter, no absolute with member in User
@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)

@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated():
        g.url = url_for('userinfo',userID = g.user.userID)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/admin/')
@admin_required
def admin():
    return render_template('admin.html')

@app.route('/<userID>/')
@login_required
def userinfo(userID):
    return render_template('index.html')

@app.route('/login/', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html',form = form)
    else:
        user = User.query.filter_by(userID = form.userID.data).first()
        if user is None:
            error = CHECK_USERID_ERROR
        elif user.password != form.password.data:
            error = CHECK_PASSWORD_ERROR
        else:
            error = None

        if error:
            return render_template('login.html',form=form, error = error)
        else:
            login_user(user)
            print repr(user) + 'login_user sucessfully'
            return redirect('/')

@app.route('/register/',methods=['GET','POST'])
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
        elif User.query.get(form.userID.data) is not None:
            error = EXIST_ERROR
        else:
            error = None

        if error:
            return render_template('register.html',form=form, error=error)
        else:
            user = User(form.userID.data, form.nickname.data,form.password.data)
            user.save()
            print 'sucessfully register!'
            login_user(user)
            return redirect('/')

@app.route('/logout/')
def logout():
    print repr(current_user) + 'logged out....'
    logout_user()
    return redirect('/')

@app.route('/problemset/')
@app.route('/problemset/page=<int:page>/')
def problemset(page = 1):
    problem_count = Problem.query.count()

    Page_Max = problem_count/3
    if problem_count % 3 != 0:
        Page_Max += 1

    if page not in range(1,Page_Max + 1):
        return 'error page'

    problem_list = Problem.query.order_by(Problem.pid)[(page - 1) * 100 : min(problem_count, page*100)]

    return render_template('problemset.html', page=page, Page_Max = Page_Max, problem_list = problem_list)

@app.route('/admin/problemset/')
@admin_required
def admin_problemset():
    return render_template('admin_problemset.html')


@app.route('/admin/problemset/addproblem/', methods=['GET','POST'])
@admin_required
def admin_addproblem():
    form = ProblemForm()
    if request.method == 'GET':
        return render_template('admin_addproblem.html',form=form)
    else:
        inputfile = request.files['inputfile']
        outputfile = request.files['outputfile']
        problem_count = Problem.query.count()
        inputfile.save(os.path.join(app.config['UPLOAD_FOLDER'], '.'.join([str(problem_count + 1),'in'])))
        outputfile.save(os.path.join(app.config['UPLOAD_FOLDER'], '.'.join([str(problem_count + 1), 'out'])))

        problem = Problem(form.title.data, form.description.data, form.pinput.data, form.poutput.data, form.sinput.data, form.soutput.data, form.hint.data)

        problem.save()

        print 'upload successfully!'

        return redirect('/admin/problemset')

