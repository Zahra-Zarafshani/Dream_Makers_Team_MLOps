
from flask import Flask, render_template, redirect, url_for, request ,flash , session
from forms import RegistrationForm , InputDataForm
from PredictionModel import PredictionModel
app = Flask(__name__)
app.config['SECRET_KEY'] = 'cancerpredictionportal'   

users_db = {'user@example.com': 'password'}


@app.route('/')
def Main():
    return  render_template('login.html')


@app.route('/register', methods=['GET' ,'POST'])
def Register():
    form = RegistrationForm()
    
    if request.method =='POST':
        if form.validate_on_submit(): 
            # Flash message for registration successfull
            return redirect(url_for('Dashboard'))
    
    return render_template('register.html', form=form )

@app.route('/login', methods=['GET' ,'POST'])
def Login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Check credentials
        if username in users_db and users_db[username] == password:
            session['user'] = username  
            return redirect(url_for('Dashboard'))
    return render_template('login.html' )
        
@app.route('/logout', methods=['GET' ,'POST'])
def Logout():
        # Remove user from session 
        # Logout flash message
        return redirect(url_for('Login'))
    
##################################################################################


@app.route('/dashboard', methods=['GET'])
def Dashboard():
        return render_template('dashboard.html'  )


@app.route('/inputdata', methods=['GET' ,'POST'])
def Inputdata():
    inputform = InputDataForm()
    
    if request.method =='POST':
        if inputform.validate_on_submit(): 
            imgfile = inputform.imgfile.data
            #save the uploaded file in upload_directory and save its info in database for further history
            feature1 = inputform.feature1.data
            #save other features in database too (for further history)
            input_object = {'imgfile': imgfile , 'feature1' :feature1}
            predict = PredictionModel(input_object)
            predicted_results =predict.computed_predictions()
            return render_template('prediction.html' , predicted_results=predicted_results )
    
    return render_template('inputdata.html', form=inputform  )


@app.route('/history', methods=['GET'])
def History():
        # extract History from database
        return render_template('history.html'  )

@app.route('/prediction', methods=['GET'])
def Prediction(predicted_results):
    return render_template('prediction.html' , predicted_results )




if __name__ == '__main__':
    app.run(debug=True)
