
from flask_wtf import FlaskForm 

from wtforms import StringField, EmailField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_wtf.file import FileAllowed, FileRequired


from wtforms import StringField, FileField, SubmitField
from wtforms.validators import DataRequired

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired('Please enter username.'), 
                                                   Length(min=3, message = ' Username must be at least 3 characters long.')])
    email = EmailField('Email', validators=[DataRequired('Please enter your Email.'), 
                                            Email(message='Email is not valid!')])
    password = PasswordField('Password', validators=[DataRequired('Please enter a password'),
                                                      Length(min=8 , message='Please enter a password with at leat 8 characters.')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired('Please confirm your password!'), 
                                                                     EqualTo('password' , message='Password mismatch!')])
    submit = SubmitField('Register')


class InputDataForm(FlaskForm):
    feature1 = StringField('Feature_1', 
                           validators=[DataRequired('Please enter value....')])
    imgfile = FileField('Scan image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
    ])
    submit = SubmitField('Predict')

    