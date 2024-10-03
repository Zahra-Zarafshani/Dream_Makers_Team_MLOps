
from flask_wtf import FlaskForm 
from wtforms import StringField, EmailField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileAllowed, FileRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired('Please enter a username.'), 
                                                   Length(min=3, max=20, message = ' Username must be at least 3 characters long.')])
    email = EmailField('Email', validators=[DataRequired('Please enter your Email.'), 
                                            Email(message='Email is not valid!')])
    password = PasswordField('Password', validators=[DataRequired('Please enter a password'),
                                                      Length(min=8 , message='Please enter a password with at leat 8 characters.')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired('Please confirm your password!'), 
                                                                     EqualTo('password' , message='Password mismatch!')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already registered. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired('Please enter your username.'), Email('Please enter your Email.')])
    password = PasswordField('Password', validators=[DataRequired('Please enter your password')])
    submit = SubmitField('Login')


class InputDataForm(FlaskForm):
    feature1 = StringField('Feature_1', 
                           validators=[DataRequired('Please enter value....')])
    imgfile = FileField('Scan image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
    ])
    submit = SubmitField('Predict')

