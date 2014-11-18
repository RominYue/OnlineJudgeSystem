#!/usr/bin/env python2
# -*- coding:utf-8 -*-

from appfile import app, login_manager, db

from flask import render_template,request,g, redirect, url_for
from flask.ext.login import login_user, logout_user, login_required, current_user
from forms import RegisterForm, LoginForm, ProblemForm, SubmissionForm, SearchProblemForm, SearchSubmitForm, PostForm, ReplyForm
from config import USERID_ERROR, NICKNAME_ERROR, PASSWORD_ERROR, EQUAL_ERROR, CHECK_USERID_ERROR, CHECK_PASSWORD_ERROR, EXIST_ERROR, PERMISSION_ERROR, INPUT_ERROR, UPLOAD_SUCESS, MAX_PROBLEM_NUM_ONE_PAGE, MAX_SUBMIT_NUM_ONE_PAGE, USER_NUM_ONE_PAGE, MAX_REPLY_NUM_ONE_PAGE
from models import User, Problem, Submit, Comment, Reply
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

@app.route('/userinfo?userid=<userID>/')
def userinfo(userID):
    user = User.query.get(userID)
    solved_problem_list = Submit.query.filter_by(userid = userID, result = 'Accepted').order_by(Submit.pid).distinct(Submit.pid).all()
    user_list = User.query.order_by(User.ac_count.desc(), User.submit_count, User.userID).all()
    rank  = user_list.index(user) + 1

    return render_template('userinfo.html', user = user, rank = rank, solved_problem_list = solved_problem_list)

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
    form = SearchProblemForm()

    problem_list = Problem.query.filter_by(visable = True).order_by(Problem.pid).paginate(page,MAX_PROBLEM_NUM_ONE_PAGE, False )

    return render_template('problemset.html', page=page, problem_list = problem_list, form = form)

@app.route('/showproblem/pid=<int:pid>/')
def show_problem(pid):
    problem = Problem.query.get(pid)
    return render_template('showproblem.html', problem=problem)

@app.route('/searchproblem/', methods =['POST'])
def search_problem():
    form = SearchProblemForm()
    if form.pid.data is None:
        return redirect('/problemset/')
    else:
        return redirect(url_for('show_problem', pid = (form.pid.data - 1000)))


@app.route('/problemstatus/')
def problemstatus():

    pid = request.args.get('pid')
    page = request.args.get('page')

    if not page:
        page = 1


    solution_list = Submit.query.filter_by(pid = pid, result = 'Accepted').order_by(Submit.time_used, Submit.memory_used).group_by(Submit.userid).paginate(page, MAX_SUBMIT_NUM_ONE_PAGE, False)

    return render_template('problemstatus.html', pid = pid, page = page, solution_list = solution_list, MAX_SUBMIT_NUM_ONE_PAGE = MAX_SUBMIT_NUM_ONE_PAGE)


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

@app.route('/status/', methods = ['GET','POST'])
@app.route('/status/page=<int:page>')
def status(page = 1):
    form = SearchSubmitForm()

    if request.method == 'POST':

        subq = Submit.query

        if form.pid.data:
            subq = subq.filter_by(pid = form.pid.data)
        if form.userid.data:
            subq = subq.filter_by(userid = form.userid.data)
        if form.language.data and form.language.data != 'All':
            subq = subq.filter_by(language = form.language.data)
        if form.result.data and form.result.data != 'All':
            subq = subq.filter_by(result = form.result.data)

        submit_list = subq.paginate(page, MAX_SUBMIT_NUM_ONE_PAGE, False)
    else:
        submit_list = Submit.query.order_by(Submit.runid.desc()).paginate(page, MAX_SUBMIT_NUM_ONE_PAGE, False)
    return render_template('status.html', submit_list = submit_list, form = form)

@app.route('/showcompileinfo/<int:runid>')
def show_compile_info(runid):
        submit = Submit.query.get(runid)
        return render_template('ce_error.html', ce_error = submit.ce_error)

@app.route('/admin/')
@admin_required
def admin():
    return render_template('admin.html')


@app.route('/admin/problemset/')
@app.route('/admin/problemset/page=<int:page>')
@admin_required
def admin_problemset(page = 1):

    problem_list = Problem.query.order_by(Problem.pid).paginate(page, MAX_PROBLEM_NUM_ONE_PAGE, False)

    return render_template('admin_problemset.html', page = page, problem_list = problem_list)

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
        Problem.query.filter_by(pid = pid).update({'title': form.title.data, 'description': form.description.data, 'pinput': form.pinput.data, 'poutput': form.poutput.data, 'sinput': form.sinput.data, 'soutput': form.soutput.data, 'hint': form.hint.data, 'time_limit': form.time_limit.data, 'memory_limit': form.memory_limit.data})
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

@app.route('/viewcode/')
def viewcode():
    runid = request.args.get('runid')
    submit = Submit.query.get(runid)
    return render_template('showcode.html',submit = submit)

@app.route('/FAQ/')
def show_faq():
    return render_template('FAQ.html')

@app.route('/ranklist/')
@app.route('/ranklist/<int:page>/')
def show_ranklist(page = 1):

    user_list = User.query.order_by(User.ac_count.desc(), User.submit_count, User.userID).paginate(page,USER_NUM_ONE_PAGE, False)

    return render_template('ranklist.html', user_list = user_list, page = page, USER_NUM_ONE_PAGE =USER_NUM_ONE_PAGE )

#@app.route('/webboard/')
#def web_board():
#    return render_template('webboard.html')


@app.route('/discuss/')
def discuss():
    pid = request.args.get('pid')
    if pid:
        comment_list = Comment.query.filter_by(pid = pid).order_by('comment.last_reply DESC').all()
    else:
        comment_list = Comment.query.order_by('comment.last_reply DESC').all()
    return render_template('discuss.html', comment_list = comment_list, pid = pid)

@app.route('/discuss/newpost/',methods = ['GET','POST'])
def newpost():
    pid = request.args.get('pid')
    form = PostForm()
    if request.method == 'GET':
        form = PostForm(pid = pid)
        return render_template('newpost.html', form = form)
    else:
        if not Problem.query.filter_by(pid = form.pid.data).all():
            return 'error'
        comment = Comment(pid = form.pid.data, userid = current_user.userID, \
                            nickname = current_user.nickname, title = form.title.data, \
                            content = form.content.data, post_time = get_now_time())
        db.session.add(comment)
        db.session.commit()

        return redirect(url_for('discuss', pid = pid))

@app.route('/comment/<int:tid>/',methods = ['GET','POST'])
def show_comment(tid):
    form = ReplyForm()
    if request.method == 'GET':
        page = request.args.get('page')
        if not page:
            page = 1
        else:
            page = int(page)
        if page == 1:
            comment = Comment.query.filter_by(tid = tid).first()
        else:
            comment = None

        title = Comment.query.filter_by(tid = tid).first().title
        reply_list = Reply.query.filter_by(tid = tid).order_by('reply.rid').paginate(page, MAX_REPLY_NUM_ONE_PAGE)
        return render_template('comment.html', tid = tid, title = title, comment = comment, page = page,reply_list = reply_list, form = form)
    else:
        reply = Reply(tid = tid, userid = current_user.userID, nickname = current_user.nickname, \
                        content = form.content.data, post_time = get_now_time())

        comment = Comment.query.filter_by(tid = tid).first()
        comment.re += 1
        db.session.add(reply)
        db.session.commit()
        return redirect(request.referrer)


@app.route('/deletepost/')
def deletepost():
    if request.args.get('tid'):
        Comment.query.filter_by(tid = request.args.get('tid')).delete()
        db.session.commit()
    elif request.args.get('rid'):
        Reply.query.filter_by(rid = request.args.get('rid')).delete()
        db.session.commit()

    return redirect('/discuss/')
