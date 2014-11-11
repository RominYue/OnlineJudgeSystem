import os

from appfile import db
from appfile.models import User
from config import ADMIN_USERID, ADMIN_NICKNAME, ADMIN_PASSWORD

#make problem directory
os.system('rm -rf appfile/problems')
os.mkdir('appfile/problems')

#init db
db.drop_all()
db.create_all()

#create admin
tmp_admin = User(userID = ADMIN_USERID, nickname = ADMIN_NICKNAME, password = ADMIN_PASSWORD, is_admin = True)
tmp_admin.save()
