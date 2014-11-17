from flask_wtf import Form
from wtforms import TextField, BooleanField, PasswordField, TextAreaField, IntegerField, StringField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo
import re

class RegisterForm(Form):
    userID = TextField('user ID')
    nickname = TextField('Nick Name')
    password = PasswordField('PassWord')
    rptpassword = PasswordField('Repeat Password')

    def validate_userID(self):
        return re.match(r'^[a-zA-Z0-9]{3,22}$',self.userID.data)

    def validate_nickname(self):
        return 5 < len(self.nickname.data) < 23

    def validate_password(self):
        return re.match(r'^[a-zA-Z0-9]{6,22}$',self.password.data)

    def validate_equal(self):
        return self.password.data == self.rptpassword.data


class LoginForm(Form):
    userID = TextField('user ID')
    password = PasswordField('Password')

    def validate_userID(self):
        return re.match(r'^[a-zA-Z0-9]{4,23}$', self.userID.data)

    def validate_password(self):
        return re.match(r'^[a-zA-Z0-9]{6,22}$', self.password.data)


class ProblemForm(Form):
    title = TextField('Title', [Length(max = 299)])
    description = TextAreaField('Description', [Length(max = 9999)])
    pinput = TextAreaField('Input', [Length(max = 9999)])
    poutput = TextAreaField('Output', [Length(max = 9999)])
    sinput = TextAreaField('Sample Input', [Length(max = 9999)])
    soutput = TextAreaField('Sample Output', [Length(max = 9999)])
    hint = TextAreaField('Hint', [Length(max = 9999)])
    time_limit = IntegerField('Time Limit',[DataRequired()])
    memory_limit = IntegerField('Memory Limit', [DataRequired()])

class SubmissionForm(Form):
    pid = IntegerField('Problem ID')
    language = SelectField('Language',choices = [('C','C'),('C++','C++'),('Python2.7','Python2.7')])
    src = TextAreaField('Source Code')

class SearchProblemForm(Form):
    pid = IntegerField('Problem ID')

class SearchSubmitForm(Form):
    pid = IntegerField('Problem ID')
    userid = TextField('UserID')
    language = SelectField(choices = [('All','All'), ('C++', 'C++'), ('C', 'C'), ('Python2.7', 'Python2.7')])
    result = SelectField(choices = [ ('All','All'), \
                                     ('Accepted', 'Accepted'), \
                                     ('Presentation Error', 'Presentation Error'), \
                                     ('Time Limit Exceeded', 'Time Limit Exceeded'), \
                                     ('Memory Limit Exceeded', 'Memory Limit Exceeded'), \
                                     ('Wrong Answer', 'Wrong Answer'), \
                                     ('Runtime Error', 'Runtime Error'), \
                                     ('Output Limit Exceeded', 'Output Limit Exceeded'), \
                                     ('Compile Error', 'Compile Error')])

