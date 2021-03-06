#!usr/bin/env python2
# _*_ coding:utf-8 _*_


import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'tmp.db')

MAIN_PATH = os.getcwd()
UPLOAD_FOLDER = os.path.join(MAIN_PATH,'appfile/problems')
TMP_FOLDER = os.path.join(MAIN_PATH, 'appfile/tmpfile')
WAIT_TIME = 0.5


CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'



EXIST_ERROR = 'User ID has been registered!'
CHECK_USERID_ERROR = 'User ID does not exist!'
CHECK_PASSWORD_ERROR = 'Password is not correct!'
PERMISSION_ERROR = "you are not admin!"
INPUT_ERROR = 'Input Limit Exceeded'
UPLOAD_SUCESS = 'Uploaded Successfully'

MAX_PROBLEM_NUM_ONE_PAGE = 2
MAX_SUBMIT_NUM_ONE_PAGE = 2
USER_NUM_ONE_PAGE = 2
MAX_REPLY_NUM_ONE_PAGE = 2


ADMIN_USERID = 'guest'
ADMIN_NICKNAME = 'guest'
ADMIN_PASSWORD = '116023'

PYTHON_TIME_LIMIT_TIMES = 10
PYTHON_MEMORY_LIMIT_TIMES = 10

JUDGE_RESULT = {
    0: 'Accepted',
    1: 'Presentation Error',
    2: 'Time Limit Exceeded',
    3: 'Memory Limit Exceeded',
    4: 'Wrong Answer',
    5: 'Runtime Error',
    6: 'Output Limit Exceeded',
    7: 'Compile Error',
    8: 'System Error'
}
