
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
    app.run(debug=True)
