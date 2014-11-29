#!usr/bin/env python2
# _*_ coding:utf-8 _*_


import time
import Queue
from appfile.judge import put_task_into_queue, work
from appfile import db
from appfile.models import Submit
from config import WAIT_TIME
if __name__ == '__main__':
    que = Queue.Queue()
    switch = 0
    while True:
        if switch:
            work(que)
        else:
            put_task_into_queue(que)
            time.sleep(WAIT_TIME)

        switch ^= 1
