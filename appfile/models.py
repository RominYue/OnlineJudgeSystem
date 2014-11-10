from appfile import db

ROLE_USER = 0
ROEL_ADMIN = 1

class User(db.Model):
    #id = db.Column(db.Integer, primary_key = True)
    userID = db.Column(db.String(22), primary_key = True, unique = True)
    nickname = db.Column(db.String(22),unique = True)
    password = db.Column(db.String(100), index = True, unique = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)

    def __init__(self, userID, nickname, password):
        self.userID = userID
        self.nickname = nickname
        self.password = password

    def __repr__(self):
        return '<User %s>' % (self.nickname)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.userID

    def save(self):
        db.session.add(self)
        db.session.commit()
