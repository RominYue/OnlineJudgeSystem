#!usr/bin/env python2
# _*_ coding:utf-8 _*_

import os
import os.path
import subprocess, shelx

from app import db
from models import Submit
from config import  UPLOAD_FOLDER, TMP_FOLDER, JUDGE_RESULT, PYTHON_TIME_LIMIT_TIMES, PYTHON_MEMORY_LIMIT_TIMES

def put_task_into_queue(que):
    submit_list = Submit.query.filter_by(result = 'Pending').order_by(Submit.runid).all()

    for submit in submit_list:
        task = {
            'runid':submit.runid,
            'pid':submit.pid,
            'language': submit.language
        }

        que.put(task)


def work(que):
    while not que.empty():
        task = que.get()
        runid = task['runid']
        pid = task['pid']
        language = task['language']
        result, rst = judge(runid,pid,language)
        if result == 'Accepted':
            db.session.query(Submit).filter_by(runid = runid).update({'result': result,'time_used': rst['timeused'], 'memory_used': rst['memoryused']})
        else:
            Submit.query.filter_by(runid = runid).update({'result':result})
        db.session.commit()

        que.task_done()


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
        #db.session.query(Submit).filter_by(runid = runid).update({'ce_error': ''.join([out, error])})
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

    input_file = file(os.path.join(UPLOAD_FOLDER, ''.join([str(pid), '.in'])))
    output_file = file(os.path.join(UPLOAD_FOLDER, ''.join([str(pid), '.out'])))
    tmp_file = file(os.path.join(TMP_FOLDER, str(runid)), 'w')
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
    rst = lorun.run(runcfg)
    tmp_file = file(os.path.join(TMP_FOLDER, str(runid)))
    return JUDGE_RESULT[lorun.check(output_file.fileno(), tmp_file.fileno())], rst


