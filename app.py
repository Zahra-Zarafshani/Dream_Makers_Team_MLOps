from flask import Flask, render_template, redirect, url_for, request, flash, session
from PredictionModel import PredictionModel , Features
from forms import RegistrationForm, InputDataForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

# app configs
app.config['SECRET_KEY'] = 'cancerpredictionportal'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

     

##############
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
##############

@app.route('/')
def Main():
    flash("Welcome!" , 'success')
    return render_template('index.html')


@app.route("/register", methods=['GET', 'POST'])
def Register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
            #check whether the username or email exists already
            user = User.query.filter_by(username=form.username.data).first()
            email = User.query.filter_by(email=form.email.data).first() 
            if user or email:
                flash(f'{form.username.data} or {form.email.data} already registered. Please try again.', 'danger')
                return redirect(url_for('Register')) 
            else: #information is ok. register a new one
                hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                user = User(username=form.username.data, email=form.email.data, password=hashed_password)
                db.session.add(user)
                db.session.commit()
                flash('Your account has been created! You can now log in.', 'success')
                return redirect(url_for('Login'))  
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def Login():
    if current_user.is_authenticated:
        return redirect(url_for('Dashboard'))
    form = LoginForm() 
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data  

        # بررسی اعتبار کاربر در دیتابیس
        user = User.query.filter_by(username=username).first() 
        if user and bcrypt.check_password_hash(user.password, password):
            session['username'] = user.username
            #login_user(user) 
            flash('Login successful!', 'success')
            return redirect(url_for('Dashboard'))
        else:
            flash('Login failed. Check your username and password.', 'danger')

    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
@login_required
def Logout():
    logout_user()
    session.pop('username')
    flash('You have been logged out.', 'info')
    return redirect(url_for('Login'))


#######################################################################

@app.errorhandler(500)
@login_required
def servererror(e): 
    return render_template('error.html' , title='Error')

##################################################################################


@app.route('/dashboard', methods=['GET'])
def Dashboard():
        return render_template('dashboard.html'  )


################################################################################## fatemeh-k
@app.route('/inputdata', methods=['GET' ,'POST'])
def Inputdata():
    inputform = InputDataForm()
    
    if request.method =='POST':
        if inputform.validate_on_submit():
            input_object = {} 
            for numfeature in Features.numerical_features: 
                    input_object[numfeature] = inputform[numfeature].data
            print("==============================")
            print(input_object)
            print("==============================")
  
            predictobj = PredictionModel(input_object)
            predicted_results =predictobj.computed_predictions()
            return render_template('prediction.html' , predicted_results=predicted_results )
        else:
            print("Form validation failed:===============================")
            print(inputform.errors) 
    
    return render_template('inputdata.html', form=inputform , Features=Features )
##################################################################################

@app.route('/history', methods=['GET'])
def History():
        # extract History from database
        return render_template('history.html'  )

################################################################################## fatemeh-k

@app.route('/prediction', methods=['GET'])
def Prediction(predicted_results):
    return render_template('prediction.html' , predicted_results )

##################################################################################

if __name__ == '__main__':
    # Create Database
    with app.app_context():
        db.create_all()
    app.run(debug=True)
