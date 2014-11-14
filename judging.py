import time
import Queue
from appfile.judge import put_task_into_queue, work
from appfile import db
from appfile.models import Submit

if __name__ == '__main__':
    que = Queue.Queue()
    switch = 0
    while True:
        if switch:
            work(que)
        else:
            put_task_into_que(que)
            time.sleep(0.5)

        switch ^= 1
