
from flask_wtf import FlaskForm 
from wtforms import StringField, EmailField, PasswordField, SubmitField, FileField , IntegerField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileAllowed, FileRequired
from PredictionModel import Features

 
 
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

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired('Please enter your username.')])
    password = PasswordField('Password', validators=[DataRequired('Please enter your password')])
    submit = SubmitField('Login')
 

 

class InputDataForm(FlaskForm):
    submit = SubmitField('Predict')

# Dynamically add NumericalFields to InputDataForm
for numfeature in Features.numerical_features:
    setattr(InputDataForm, numfeature, 
            FloatField(numfeature, validators=[DataRequired("Please enter value....")]))

for feature in Features.file_features:
    setattr(InputDataForm, feature, 
            FileField(feature, validators=[FileRequired(), FileAllowed(['jpg', 'jpeg'], 'Images only!')]))


    
 
