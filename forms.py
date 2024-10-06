
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
    ################################################################################## Falaki
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
    diagnosis = StringField('diagnosis', 
                           validators=[DataRequired('Please enter value....')])
    radius_mean = StringField('radius_mean', 
                           validators=[DataRequired('Please enter value....')])
    texture_mean = StringField('texture_mean', 
                           validators=[DataRequired('Please enter value....')])
    perimeter_mean = StringField('perimeter_mean', 
                           validators=[DataRequired('Please enter value....')])
    area_mean = StringField('area_mean', 
                           validators=[DataRequired('Please enter value....')])
    smoothness_mean = StringField('smoothness_mean', 
                           validators=[DataRequired('Please enter value....')])
    compactness_mean = StringField('compactness_mean', 
                           validators=[DataRequired('Please enter value....')])
    concavity_mean = StringField('concavity_mean', 
                           validators=[DataRequired('Please enter value....')])
    concave_points_mean = StringField('concave_points_mean', 
                           validators=[DataRequired('Please enter value....')])
    symmetry_mean = StringField('symmetry_mean', 
                           validators=[DataRequired('Please enter value....')])
    fractal_dimension_mean = StringField('fractal_dimension_mean', 
                           validators=[DataRequired('Please enter value....')])
    radius_se = StringField('radius_se', 
                           validators=[DataRequired('Please enter value....')])
    texture_se = StringField('texture_se', 
                           validators=[DataRequired('Please enter value....')])
    perimeter_se = StringField('perimeter_se', 
                           validators=[DataRequired('Please enter value....')])
    area_se = StringField('area_se', 
                           validators=[DataRequired('Please enter value....')])
    smoothness_se = StringField('smoothness_se', 
                           validators=[DataRequired('Please enter value....')])
    compactness_se = StringField('compactness_se', 
                           validators=[DataRequired('Please enter value....')])
    concavity_se = StringField('concavity_se', 
                           validators=[DataRequired('Please enter value....')])
    concave_points_se = StringField('concave_points_se', 
                           validators=[DataRequired('Please enter value....')])
    symmetry_se = StringField('symmetry_se', 
                           validators=[DataRequired('Please enter value....')])
    fractal_dimension_se = StringField('fractal_dimension_se', 
                           validators=[DataRequired('Please enter value....')])
    radius_worst = StringField('radius_worst', 
                           validators=[DataRequired('Please enter value....')])
    perimeter_worst = StringField('perimeter_worst', 
                           validators=[DataRequired('Please enter value....')])
    area_worst = StringField('area_worst', 
                           validators=[DataRequired('Please enter value....')])
    smoothness_worst = StringField('smoothness_worst', 
                           validators=[DataRequired('Please enter value....')])
    compactness_worst = StringField('compactness_worst', 
                           validators=[DataRequired('Please enter value....')])
    concavity_worst = StringField('concavity_worst', 
                           validators=[DataRequired('Please enter value....')])
    concave_points_worst = StringField('concave_points_worst', 
                           validators=[DataRequired('Please enter value....')])
    symmetry_worst = StringField('symmetry_worst', 
                           validators=[DataRequired('Please enter value....')])
    fractal_dimension_worst = StringField('fractal_dimension_worst', 
                           validators=[DataRequired('Please enter value....')])
    
    
    imgfile = FileField('Scan image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
    ])
    submit = SubmitField('Predict')
 
