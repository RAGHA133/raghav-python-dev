from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Load configuration
app.config.from_pyfile('config.py')

# Initialize the db with app
db.init_app(app)

# Import models after db is initialized
from models.user_model import User

# ✅ Inject current datetime into all templates
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(f"[DEBUG] Login attempt: username={username}, password={password}")

        user = User.query.filter_by(name=username).first()
        print(f"[DEBUG] Retrieved user: {user}")

        if user:
            print(f"[DEBUG] User found. DB password hash: {user.password}")
            match = check_password_hash(user.password, password)
            print(f"[DEBUG] Password match: {match}")
        else:
            print("[DEBUG] No user found with that name.")

        if user and check_password_hash(user.password, password):
            session['username'] = user.name
            print("[DEBUG] Login successful!")
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials')
            print("[DEBUG] Login failed. Redirecting back to login.")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        user = User.query.filter_by(name=session['username']).first()
        return render_template('dashboard.html', user=user)
    else:
        return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/reset-db')
def reset_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
    return 'Database has been reset.'

@app.route('/employees/salary')
def filter_employees_by_salary():
    min_salary = request.args.get('min', type=float)
    return f"Employees with salary >= {min_salary}"

@app.route('/.well-known/appspecific/com.chrome.devtools.json')
def chrome_devtools_json():
    return '', 204  # No content

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
