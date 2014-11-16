#!usr/bin/env python2
# _*_ coding:utf-8 _*_

import os
import os.path
import subprocess, shlex
import lorun

from appfile import db
from models import Submit, Problem, User
from config import  UPLOAD_FOLDER, TMP_FOLDER, JUDGE_RESULT, PYTHON_TIME_LIMIT_TIMES, PYTHON_MEMORY_LIMIT_TIMES


def rm_tmp_file(runid):
    os.system(' '.join(['rm', os.path.join(TMP_FOLDER, str(runid))]))


def put_task_into_queue(que):
    submit_list = Submit.query.filter_by(result = 'Pending').order_by(Submit.runid).all()

    for submit in submit_list:
        task = {
            'runid':submit.runid,
            'pid':submit.pid,
            'language': submit.language,
            'userid': submit.userid
        }

        que.put(task)


def work(que):
    while not que.empty():
        task = que.get()
        runid = task['runid']
        pid = task['pid']
        language = task['language']
        userid = task['userid']

        result, rst = judge(runid,pid,language)

        problem = Problem.query.get(pid)
        user = User.query.get(userid)

        if result == 'Accepted':

            if not Submit.query.filter_by(pid = pid, userid = userid, result = 'Accepted').all():
                user.ac_count += 1

            problem.ac_count += 1
            db.session.query(Submit).filter_by(runid = runid).update({'result': result,'time_used': rst['timeused'], 'memory_used': rst['memoryused']})
        else:
            Submit.query.filter_by(runid = runid).update({'result':result})

        problem.submit_count += 1
        user.submit_count += 1
        db.session.commit()

        que.task_done()
        rm_tmp_file(runid)


def get_code(runid, file_name):
    fout = open(os.path.join(TMP_FOLDER,file_name),'w')
    fout.write(Submit.query.get(runid).src)
    fout.close()

def compile(runid, language):

    build_cmd = {
        'C': 'gcc main.c -o main -Wall -lm -O2 -std=c99 --static -DONLINE_JUDGE',
        'C++': 'g++ main.cpp -o main -O2 -Wall -lm --static -DONLINE_JUDGE',
        'Python2.7': 'python2.7 -m py_compile main.py'
    }

    p = subprocess.Popen(build_cmd[language], shell = True, cwd = TMP_FOLDER, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    output,outerror = p.communicate()

    if p.returncode == 0:
        return True
    else:
        #error = ''.join([output,outerror])
        #Submit.query.filter_by(runid = runid).update({'ce_error': error})
        #db.session.commit()
        return False

def judge(runid, pid, language):
    filename = {
        'C':'main.c',
        'C++': 'main.cpp',
        'Python2.7':'main.py'
    }
    #form the src into main.py/main.c
    get_code(runid, filename[language])

    input_file = open(os.path.join(UPLOAD_FOLDER, ''.join([str(pid), '.in'])))
    output_file = open(os.path.join(UPLOAD_FOLDER, ''.join([str(pid), '.out'])))
    tmp_file = open(os.path.join(TMP_FOLDER, str(runid)), 'w')
    time_limit = Problem.query.get(pid).time_limit
    memory_limit = Problem.query.get(pid).memory_limit

    if not compile(runid, language):
        return ('Compile Error', None)

    if language == 'Python2.7':
        time_limit *= PYTHON_TIME_LIMIT_TIMES
        memory_limit *= PYTHON_MEMORY_LIMIT_TIMES
        cmd = 'python2.7 %s' % (os.path.join(TMP_FOLDER, 'main.pyc'))
        main_exe = shlex.split(cmd)

    else:
        main_exe = [os.path.join(TMP_FOLDER, 'main'), ]

    runcfg = {
        'args': main_exe,
        'fd_in': input_file.fileno(),
        'fd_out': tmp_file.fileno(),
        'timelimit': time_limit,
        'memorylimit': memory_limit
    }
    #lorun.run() returns a dict = {'memoryused': kb, 'timeused': ms, 'results': '0 if run properly'}
    #otherwise non-zero maybe Runtime Error
    rst = lorun.run(runcfg)
    print rst
    input_file.close()
    tmp_file.close()

    tmp_file = open(os.path.join(TMP_FOLDER, str(runid)))

    if rst['result'] == 0:
        #lorun.check() returns a number which means the final result
        crst = lorun.check(output_file.fileno(), tmp_file.fileno())
        output_file.close()
        tmp_file.close()
        rst['result'] = crst

        print crst

    return JUDGE_RESULT[rst['result']], rst


