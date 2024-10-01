import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


# تابع برای ایجاد جداول کاربران و پیش‌بینی‌ها
def create_tables():
    conn = sqlite3.connect('cancer_predictions.db')
    cursor = conn.cursor()
    
    # جدول کاربران
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,  -- رمز عبور به صورت هش‌شده ذخیره می‌شود
            email TEXT UNIQUE NOT NULL
        )
    ''')
    
    # جدول پیش‌بینی‌ها
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            input_data TEXT,
            prediction TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    conn.commit()
    conn.close()


# تابع برای ثبت کاربر جدید (با هش کردن رمز عبور)
def register_user(username, password, email):
    conn = sqlite3.connect('cancer_predictions.db')
    cursor = conn.cursor()
    
    # هش کردن رمز عبور
    hashed_password = generate_password_hash(password)
    
    try:
        cursor.execute('''
            INSERT INTO users (username, password, email) 
            VALUES (?, ?, ?)
        ''', (username, hashed_password, email))
        conn.commit()
    except sqlite3.IntegrityError:
        print("Error: Username or Email already exists.")
    
    conn.close()


# تابع برای اعتبارسنجی ورود کاربر
def authenticate_user(username, password):
    conn = sqlite3.connect('cancer_predictions.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, password FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    
    conn.close()
    
    if user and check_password_hash(user[1], password):
        return user[0]  # بازگشت user_id در صورت موفقیت
    else:
        return None


# تابع برای ذخیره‌سازی پیش‌بینی‌ها
def store_prediction(user_id, input_data, prediction):
    conn = sqlite3.connect('cancer_predictions.db')
    cursor = conn.cursor()
    
    input_data_str = str(input_data)  # تبدیل داده‌های ورودی به رشته
    
    cursor.execute('''
        INSERT INTO predictions (user_id, input_data, prediction, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (user_id, input_data_str, prediction, datetime.now()))
    
    conn.commit()
    conn.close()


# تابع برای بازیابی پیش‌بینی‌های یک کاربر خاص
def get_user_predictions(user_id):
    conn = sqlite3.connect('cancer_predictions.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT input_data, prediction, timestamp 
        FROM predictions 
        WHERE user_id = ?
    ''', (user_id,))
    
    predictions = cursor.fetchall()
    conn.close()
    
    return predictions
