#!usr/bin/env python2
# _*_ coding:utf-8 _*_

from app import db
from models import Submit

def put_task_into_queue(que):
    submit_list = Submit.query.filter_by(result = 'Pending').order_by(Submit.runid).all()

    for submit in submit_list:
        task = {
            'runid':submit.runid,
            'pid':submit.pid
        }

        que.put(task)


def work(que):
    while not que.empty():
        task = que.get()
        runid = task['runid']
        pid = task['pid']
        #result = judge()
        result = 'Accepted'
        submit = Submit.query.get(pid)
        submit.result =  result
        db.ssession.commit()
        que.task_done()

