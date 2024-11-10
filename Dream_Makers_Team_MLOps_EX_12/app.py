from flask import Flask, render_template, redirect, url_for, request, flash, session
from PredictionModel import PredictionModel , Features
from forms import RegistrationForm, InputDataForm, LoginForm
import database

app = Flask(__name__)

# app configs
app.config['SECRET_KEY'] = 'cancerpredictionportal'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = database.db
db.init_app(app)

@app.before_request
def login_required_pages():
    login_required_routes = ['/dashboard' , '/history', '/inputdata' , '/prediction'] 
    if 'username' not in session and request.path in login_required_routes:
         return redirect(url_for('Login'))


@app.route('/')
def Main():
    flash("Welcome!" , 'success')
    return render_template('index.html')


@app.route("/register", methods=['GET', 'POST'])
def Register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            registered_user = database.register_user(username, email , password) 

            if registered_user!=None :
                message = 'Your account has been created! You can now log in.'
                message_stat = 'success'
                redirect_page = 'Login'
            else:
                message = message = f'{username} or {email} already registered. Please try again.'
                message_stat = 'danger'
                redirect_page = 'Register'

            flash(message, message_stat)
            return redirect(url_for(redirect_page))
            
    # for 'GET'request:
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def Login():
    if 'username' in session:
        flash('You are already logged in.')
        return redirect(url_for('Dashboard'))
    form = LoginForm() 
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user =  database.valid_user_check(username , password)
        if user:
            session['username'] = user.username
            #login_user(user) 
            flash('Login successful!', 'success')
            return redirect(url_for('Dashboard'))
        else:
            flash('Login failed. Check your username and password.', 'danger')

    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def Logout():
    db.session.close()
    db.session.commit()
    session.pop('username')
    #logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('Login' , _method ='GET'))  


#######################################################################

@app.errorhandler(500)
def servererror(e): 
    return render_template('error.html' , title='Error')

##################################################################################

@app.route('/dashboard', methods=['GET'])
def Dashboard():
        return render_template('dashboard.html' )


################################################################################## fatemeh-k
@app.route('/inputdata', methods=['GET' ,'POST'])
def Inputdata():
    inputform = InputDataForm()
    
    if request.method =='POST':
        if inputform.validate_on_submit():
            input_object = {} 
            for numfeature in Features.numerical_features: 
                    input_object[numfeature] = inputform[numfeature].data
  
            predictobj = PredictionModel(input_object)
            predicted_results =predictobj.computed_predictions()
            print(predicted_results)
            database.store_prediction(session['username'], input_object, *predicted_results.values())
            flash('Your prediction is stored in your History.' , 'success')
            return render_template('prediction.html' , predicted_results=predicted_results )
        
    
    return render_template('inputdata.html', form=inputform , Features=Features )
##################################################################################

@app.route('/history', methods=['GET'])
def History():
        # extract History from database
        print(session['username'] , "ddddddddddddddddddddddddddddddddddddddddd")
        all_preds = database.get_user_predictions(username = session['username'])
        return render_template('history.html' , predictions=all_preds , 
                               num_features= Features.numerical_features )

################################################################################## fatemeh-k

@app.route('/prediction', methods=['GET'])
def Prediction(predicted_results):
    return render_template('prediction.html' , predicted_results )

##################################################################################

if __name__ == '__main__':
    # Create Database
    with app.app_context(): 
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
