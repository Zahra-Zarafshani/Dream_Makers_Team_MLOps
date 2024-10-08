from flask import Flask, render_template, redirect, url_for, request, flash
from PredictionModel import PredictionModel
from forms import RegistrationForm, InputDataForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
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
    return render_template('login.html')


@app.route("/register", methods=['GET', 'POST'])
def Register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('Dashboard'))  # Redirect to Dashboard page after registration
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def Login():
    if current_user.is_authenticated:
        return redirect(url_for('Dashboard'))

    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = request.form.get('username')
        password = request.form.get('password')

        # بررسی اعتبار کاربر در دیتابیس
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('Dashboard'))
        else:
            flash('Login failed. Check your username and password.', 'danger')

    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
@login_required
def Logout():
    logout_user()
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
            imgfile = inputform.imgfile.data
            #save the uploaded file in upload_directory and save its info in database for further history
            feature1 = inputform.feature1.data
            diagnosis = inputform.diagnosis.data
            radius_mean = inputform.radius_mean.data
            texture_mean = inputform.texture_mean.data
            perimeter_mean = inputform.perimeter_mean.data
            area_mean = inputform.area_mean.data
            smoothness_mean = inputform.smoothness_mean.data
            compactness_mean = inputform.compactness_mean.data
            concavity_mean = inputform.concavity_mean.data
            concave_points_mean = inputform.concave_points_mean.data
            symmetry_mean = inputform.symmetry_mean.data
            fractal_dimension_mean = inputform.fractal_dimension_mean.data
            radius_se = inputform.radius_se.data
            texture_se = inputform.texture_se.data
            perimeter_se = inputform.perimeter_se.data
            area_se = inputform.area_se.data
            smoothness_se = inputform.smoothness_se.data
            compactness_se = inputform.compactness_se.data
            concavity_se = inputform.concavity_se.data
            concave_points_se = inputform.concave_points_se.data
            symmetry_se = inputform.symmetry_se.data
            fractal_dimension_se = inputform.fractal_dimension_se.data
            radius_worst = inputform.radius_worst.data
            perimeter_worst = inputform.perimeter_worst.data
            area_worst = inputform.area_worst.data
            smoothness_worst = inputform.smoothness_worst.data
            compactness_worst = inputform.compactness_worst.data
            concavity_worst = inputform.concavity_worst.data
            concave_points_worst = inputform.concave_points_worst.data
            symmetry_worst = inputform.symmetry_worst.data
            fractal_dimension_worst = inputform.fractal_dimension_worst.data
            
            #save other features in database too (for further history)
            input_object = {
                            'imgfile': imgfile , 
                            'feature1' :feature1 , 
                            'diagnosis' :diagnosis , 'radius_mean' :radius_mean ,
                            'texture_mean' :texture_mean , 'perimeter_mean' :perimeter_mean ,
                            'area_mean' :area_mean , 'smoothness_mean' :smoothness_mean , 'compactness_mean' :compactness_mean , 
                            'concavity_mean' :concavity_mean , 'concave_points_mean' :concave_points_mean , 'symmetry_mean' :symmetry_mean , 
                            'fractal_dimension_mean' :fractal_dimension_mean , 'radius_se' :radius_se , 'texture_se' :texture_se , 'perimeter_se' :perimeter_se , 
                            'area_se' :area_se , 'smoothness_se' :smoothness_se , 'compactness_se' :compactness_se , 'concavity_se' :concavity_se , 
                            'concave_points_se' :concave_points_se , 'symmetry_se' :symmetry_se , 'fractal_dimension_se' :fractal_dimension_se , 'radius_worst' :radius_worst , 
                            'perimeter_worst' :perimeter_worst , 'area_worst' :area_worst , 'smoothness_worst' :smoothness_worst , 'compactness_worst' :compactness_worst , 
                            'concavity_worst' :concavity_worst , 'concave_points_worst' :concave_points_worst , 'symmetry_worst' :symmetry_worst , 'fractal_dimension_worstt' :fractal_dimension_worst

                            }

            predict = PredictionModel(input_object)
            predicted_results =predict.computed_predictions()
            return render_template('prediction.html' , predicted_results=predicted_results )
    
    return render_template('inputdata.html', form=inputform  )
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
