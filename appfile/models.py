from appfile import db

class User(db.Model):
    userid = db.Column(db.String(22), primary_key = True, unique = True)
    nickname = db.Column(db.String(22),unique = True)
    password = db.Column(db.String(100),unique = True)
    is_admin = db.Column(db.Boolean)
    ac_count = db.Column(db.Integer, default = 0)
    submit_count = db.Column(db.Integer, default = 0)

    def __init__(self, userid, nickname, password, is_admin = False):
        self.userid = userid
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
        return self.userid

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


class Submit(db.Model):
    runid = db.Column(db.Integer, primary_key = True)
    userid = db.Column(db.String(22))
    pid = db.Column(db.Integer)
    result = db.Column(db.String(22), default = 'Pending')
    memory_used = db.Column(db.Integer, default = None)
    time_used = db.Column(db.Integer, default = None)
    language = db.Column(db.String(22))
    src = db.Column(db.Text)
    length = db.Column(db.Integer)
    submit_time = db.Column(db.String(22))
    ce_error = db.Column(db.Text, default = None)

    def __init__(self, runid, userid, pid, language, src, submit_time):
        self.runid = runid
        self.userid = userid
        self.pid = pid
        self.language = language
        self.src = src
        self.length = len(src)
        self.submit_time = submit_time

    def save(self):
        db.session.add(self)
        db.session.commit()


class Comment(db.Model):

    tid = db.Column(db.Integer, primary_key = True)
    pid = db.Column(db.Integer)
    userid = db.Column(db.String(22))
    nickname = db.Column(db.String(22))
    title = db.Column(db.String(32))
    content = db.Column(db.Text)
    post_time = db.Column(db.String(19))
    last_reply = db.Column(db.String(19))
    re = db.Column(db.Integer, default = 0)
    replys = db.relationship('Reply', backref = db.backref('comment'))

    def __init__(self, pid, userid, nickname, title, content, post_time):
        self.pid = pid
        self.userid = userid
        self.nickname = nickname
        self.title = title
        self.content = content
        self.post_time = post_time
        self.last_reply = post_time


    def save(self):
        db.session.add(self)
        db.session.commit()

class Reply(db.Model):

    rid = db.Column(db.Integer, primary_key = True)
    tid = db.Column(db.Integer, db.ForeignKey('comment.tid', ondelete = 'CASCADE'))
    userid = db.Column(db.String(22))
    nickname = db.Column(db.String(22))
    content = db.Column(db.Text)
    post_time = db.Column(db.String(19))

    def __init__(self, tid, userid, nickname, content, post_time):
        self.tid = tid
        self.userid = userid
        self.nickname = nickname
        self.content = content
        self.post_time = post_time

    def save(self):
        db.session.add(self)
        db.session.commit()

