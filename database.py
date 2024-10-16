import sqlite3
from datetime import datetime
from PredictionModel import Features 

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
db = SQLAlchemy()
bcrypt = Bcrypt()

#========================================================================
# USER TABLE
#========================================================================
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

def valid_user_check(username , password):
    user = User.query.filter_by(username=username).first() 
    if user and bcrypt.check_password_hash(user.password, password):
        return user
    else:
        return None  

def register_user(username, email , password):
#check whether the username or email exists already
    username_founded = User.query.filter_by(username=username).first()
    email_founded = User.query.filter_by(email=email).first() 
    if username_founded or email_founded: 
        return None
    else: #information is ok. register a new user in database
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return(user)

    
#========================================================================
# HISTORY TABLE 
#========================================================================
class History(db.Model):
    __tablename__ = 'history'
    pred_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    prediction = db.Column(db.String(60), nullable=False)
    pred_time = db.Column(db.DateTime)

for numfeature in Features.numerical_features:
        setattr(History, numfeature, 
                db.Column(db.Float , nullable = False ))

#=========================================================================

# تابع برای ذخیره‌سازی پیش‌بینی‌ها
def store_prediction(username, input_object, predicted_val):
    founded_user_id = User.query.filter_by(username=username).first().id 
    hist_record = input_object
    hist_record['user_id'] = founded_user_id 
    hist_record['prediction'] = predicted_val
    hist_record['pred_time'] = datetime.now()
    hist_record = History(**hist_record)
    db.session.add(hist_record)
    db.session.commit()
    return(hist_record)


# تابع برای بازیابی پیش‌بینی‌های یک کاربر خاص
def get_user_predictions(username):
    founded_user_id = User.query.filter_by(username=username).first().id
    founded_history = History.query.filter_by(user_id=founded_user_id).all()
    for item in founded_history:
        print(type(item) , len(founded_history))
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    return founded_history
