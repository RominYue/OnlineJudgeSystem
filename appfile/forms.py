from flask_wtf import Form
from wtforms import TextField, BooleanField, PasswordField, TextAreaField, IntegerField, StringField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length, EqualTo, InputRequired
import re

class RegisterForm(Form):
    userid = TextField('User ID', validators=[
        InputRequired('Plsease enter IDs'),
        Length(min = 4, max = 25,message='length must between 4 and 25')
    ])
    nickname = TextField('Nickname', validators=[
        InputRequired('Please enter nickname'),
        Length(min = 4, max = 25,message='length must between 4 and 25')
    ])
    password = PasswordField('Password', validators=[
        InputRequired('Please enter password'),
        Length(min = 6, max = 16,message='length must between 6 and 25')
    ])
    rptpassword = PasswordField('Confirm', validators=[
        InputRequired('Enter password to confirm'),
        Length(min = 4, max = 16,message='length must between 6 and 25'),
        EqualTo('password','Password must be match')
    ])

    #def validate_userID(self):
    #    return re.match(r'^[a-zA-Z0-9]{3,22}$',self.userID.data)

    #def validate_nickname(self):
    #    return 5 < len(self.nickname.data) < 23

    #def validate_password(self):
    #    return re.match(r'^[a-zA-Z0-9]{6,22}$',self.password.data)

    #def validate_equal(self):
    #    return self.password.data == self.rptpassword.data


class LoginForm(Form):
    userid = TextField('User ID', validators=[
        InputRequired('Plsease enter IDs'),
    ])
    password = PasswordField('Password', validators=[
        InputRequired('Please enter password'),
    ])
    next_url = HiddenField()

    #def validate_userID(self):
    #    return re.match(r'^[a-zA-Z0-9]{4,23}$', self.userID.data)

    #def validate_password(self):
    #    return re.match(r'^[a-zA-Z0-9]{6,22}$', self.password.data)

class ModifyUserForm(Form):
    userid = TextField('User ID')
    nickname = TextField('Nickname', validators=[
        InputRequired('Please enter nickname'),
        Length(min = 4, max = 25,message='length must between 4 and 25')
    ])
    password = PasswordField('NewPassword', validators=[
        InputRequired('Please enter password'),
        Length(min = 6, max = 16,message='length must between 6 and 25')
    ])
    rptpassword = PasswordField('Confirm', validators=[
        InputRequired('Enter password to confirm'),
        Length(min = 4, max = 16,message='length must between 6 and 25'),
        EqualTo('password','Password must be match')
    ])


class ProblemForm(Form):
    title = TextField('Title', validators=[
        InputRequired('Title is needed for this problem'),
        Length(max = 299, message='The max length is not over 300')
    ])
    description = TextAreaField('Description', [
        Length(max = 9999,  message='The max length is not over 10000')
    ])
    pinput = TextAreaField('Input', [
        Length(max = 9999, message='The max length is not over 10000')
    ])
    poutput = TextAreaField('Output', [
        Length(max = 9999,message='The max length is not over 10000')
    ])
    sinput = TextAreaField('Sample Input', [
        Length(max = 9999,message='The max length is not over 10000')
    ])
    soutput = TextAreaField('Sample Output', [
        Length(max = 9999,message='The max length is not over 10000')
    ])
    hint = TextAreaField('Hint', [
        Length(max = 9999,message='The max length is not over 10000')
    ])
    time_limit = IntegerField('Time Limit',[
        DataRequired('You must set the value of time_limit')
    ])
    memory_limit = IntegerField('Memory Limit', [
        DataRequired('You must set the value of memory_limit')
    ])

class SubmissionForm(Form):
    pid = IntegerField('Problem ID')
    language = SelectField('Language',choices = [('C','C'),('C++','C++'),('Python2.7','Python2.7')])
    src = TextAreaField('Source Code',[
        DataRequired('No Source Code')
    ])

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


class PostForm(Form):
    pid = IntegerField()
    title = StringField()
    content = TextAreaField()

class ReplyForm(Form):
    content = TextField()

