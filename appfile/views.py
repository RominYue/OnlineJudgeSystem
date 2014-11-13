#!/usr/bin/env python2
# -*- coding:utf-8 -*-

from appfile import app, login_manager, db

from flask import render_template,request,g, redirect, url_for
from flask.ext.login import login_user, logout_user, login_required, current_user
from forms import RegisterForm, LoginForm, ProblemForm, SubmissionForm
from config import USERID_ERROR, NICKNAME_ERROR, PASSWORD_ERROR, EQUAL_ERROR, CHECK_USERID_ERROR, CHECK_PASSWORD_ERROR, EXIST_ERROR, PERMISSION_ERROR, INPUT_ERROR, UPLOAD_SUCESS
from models import User, Problem, Submit
from functools import wraps
import os,time

def admin_required(func):
    @wraps(func)
    def check(*args, **kw):
        if current_user.is_authenticated() and current_user.is_admin:
            return func(*args,**kw)
        else:
            return PERMISSION_ERROR

    return check

def delete_data(file_name):
    os.system('/'.join(['rm problems',file_name]))

def get_now_time():
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

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

    problem_list = Problem.query.filter_by(visable = True).order_by(Problem.pid)[(page - 1) * 3 : min(problem_count, page*3)]

    return render_template('problemset.html', page=page, Page_Max = Page_Max, problem_list = problem_list)

@app.route('/showproblem/pid=<int:pid>/')
def show_problem(pid):
    problem = Problem.query.get(pid)
    return render_template('showproblem.html', problem=problem)

@app.route('/submit/pid=<int:pid>/', methods=['GET','POST'])
@login_required
def submit_problem(pid):
    form = SubmissionForm(pid = pid)
    if request.method == 'GET':
        return render_template('submit.html',form = form,pid = pid)
    else:
        submit = Submit(runid = Submit.query.count() + 1, userid = current_user.userID,pid = form.pid.data, language = form.language.data, src = form.src.data, submit_time = get_now_time())

        submit.save()

        print "submit successfully"

        return redirect('/status/')

@app.route('/status/')
def status():
    return render_template('status.html')

@app.route('/admin/')
@admin_required
def admin():
    return render_template('admin.html')


@app.route('/admin/problemset/')
@app.route('/admin/problemset/page=<int:page>')
@admin_required
def admin_problemset(page = 1):
    problem_count = Problem.query.count()

    Page_Max = problem_count/3
    if problem_count % 3 != 0:
        Page_Max += 1

    if page not in range(1,Page_Max + 1) and problem_count != 0:
        return 'error page'

    problem_list = Problem.query.order_by(Problem.pid)[(page - 1) * 3 : min(problem_count, page*3)]

    return render_template('admin_problemset.html', page=page, Page_Max = Page_Max, problem_list = problem_list)

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

        problem = Problem(form.title.data, form.description.data, form.pinput.data, form.poutput.data, form.sinput.data, form.soutput.data, form.hint.data, form.time_limit.data, form.memory_limit.data)

        problem.save()

        print 'upload successfully!'

        return redirect('/admin/problemset')

@app.route('/admin/editproblem/<int:pid>/', methods=['GET','POST'])
@admin_required
def admin_edit_problem(pid):
    form = ProblemForm()
    if request.method == 'GET':
        problem = Problem.query.get(pid)
        form = ProblemForm(title = problem.title, description = problem.description, pinput = problem.pinput, poutput = problem.poutput, sinput = problem.sinput, soutput = problem.soutput, hint = problem.hint, time_limit = problem.time_limit, memory_limit = problem.memory_limit)

        return render_template('admin_editproblem.html', form = form, pid = pid)
    else:
        delete_data('.'.join([str(pid),'in']))
        delete_data('.'.join([str(pid),'out']))
        inputfile = request.files['inputfile']
        outputfile = request.files['outputfile']
        inputfile.save(os.path.join(app.config['UPLOAD_FOLDER'], '.'.join([str(pid),'in'])))
        outputfile.save(os.path.join(app.config['UPLOAD_FOLDER'], '.'.join([str(pid), 'out'])))
        problem = Problem.query.get(pid)
        problem.title = form.title.data
        problem.description = form.description.data
        problem.pinput = form.pinput.data
        problem.poutput = form.poutput.data
        problem.sinput = form.sinput.data
        problem.soutput = form.soutput.data
        problem.hint = form.hint.data
        problem.time_limit = form.time_limit.data
        problem.memory_limit = form.memory_limit.data
        db.session.commit()

        return redirect('/admin/problemset')

@app.route('/admin/hideproblem/<int:pid>/')
@admin_required
def admin_hide_problem(pid):
    problem = Problem.query.get(pid)
    problem.visable = False
    db.session.commit()
    print problem.visable
    return redirect('/admin/problemset')


@app.route('/admin/displayproblem/<int:pid>/')
@admin_required
def admin_display_problem(pid):
    problem = Problem.query.get(pid)
    problem.visable = True
    db.session.commit()
    return redirect('/admin/problemset')

