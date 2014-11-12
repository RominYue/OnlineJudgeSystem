from appfile import db

class User(db.Model):
    #id = db.Column(db.Integer, primary_key = True)
    userID = db.Column(db.String(22), primary_key = True, unique = True)
    nickname = db.Column(db.String(22),unique = True)
    password = db.Column(db.String(100), index = True, unique = True)
    is_admin = db.Column(db.Boolean)

    def __init__(self, userID, nickname, password, is_admin = False):
        self.userID = userID
        self.nickname = nickname
        self.password = password
        self.is_admin = is_admin

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


class Problem(db.Model):
    pid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(299))
    description = db.Column(db.Text)
    pinput = db.Column(db.Text)
    poutput = db.Column(db.Text)
    sinput = db.Column(db.Text)
    soutput = db.Column(db.Text)
    hint = db.Column(db.Text)
    time_limit = db.Column(db.Integer)
    memory_limit = db.Column(db.Integer)
    ac_count = db.Column(db.Integer, default = 0)
    submit_count = db.Column(db.Integer, default = 0)
    visable = db.Column(db.Boolean, default = True)

    def __init__(self, title, description, pinput, poutput, sinput, soutput, hint,time_limit, memory_limit):
        self.title = title
        self.description = description
        self.pinput = pinput
        self.poutput = poutput
        self.sinput = sinput
        self.soutput = soutput
        self.hint = hint
        self.time_limit = time_limit
        self.memory_limit = memory_limit

    def save(self):
        db.session.add(self)
        db.session.commit()


