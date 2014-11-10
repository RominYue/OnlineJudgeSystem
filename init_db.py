from appfile import db
from appfile.models import User
from config import ADMIN_USERID, ADMIN_NICKNAME, ADMIN_PASSWORD

db.drop_all()
db.create_all()

tmp_admin = User(userID = ADMIN_USERID, nickname = ADMIN_NICKNAME, password = ADMIN_PASSWORD, is_admin = True)
tmp_admin.save()
