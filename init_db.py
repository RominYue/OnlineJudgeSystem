import os

from appfile import db
from appfile.models import User
from config import ADMIN_USERID, ADMIN_NICKNAME, ADMIN_PASSWORD, UPLOAD_FOLDER, TMP_FOLDER

#make problem directory
os.system(' '.join(['rm -rf', UPLOAD_FOLDER]))
os.system(' '.join(['rm -rf', TMP_FOLDER]))
os.mkdir(UPLOAD_FOLDER)
os.mkdir(TMP_FOLDER)

#init db
db.drop_all()
db.create_all()

#create admin
tmp_admin = User(userid = ADMIN_USERID, nickname = ADMIN_NICKNAME, password = ADMIN_PASSWORD, is_admin = True)
tmp_admin.save()
