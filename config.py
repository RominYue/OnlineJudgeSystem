import os.path

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'tmp.db')
UPLOAD_FOLDER = 'appfile/problems'

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

USERID_ERROR = 'User ID can only contain NUMBERs & LETTERs and length must be 3 to 22.'
NICKNAME_ERROR = 'Nick Name must be 6 to 22 characters.'
PASSWORD_ERROR = 'Password can only contain NUMBERs & LETTERs and length must be 6 to 22.'
EQUAL_ERROR = 'Repeat PassWord must be equal to PassWord'
EXIST_ERROR = 'User ID has been registered!'
CHECK_USERID_ERROR = 'User ID does not exist!'
CHECK_PASSWORD_ERROR = 'Password is not correct!'
PERMISSION_ERROR = "you are not admin!"
INPUT_ERROR = 'Input Limit Exceeded'
UPLOAD_SUCESS = 'Uploaded Successfully'

PING = 'Pending'
MAX_PROBLEM_NUM_ONE_PAGE = 3
MAX_SUBMIT_NUM_ONE_PAGE = 3
ADMIN_USERID = 'guest'
ADMIN_NICKNAME = 'guest'
ADMIN_PASSWORD = '116023'
