from flask import render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from extensions import db
from models.user_model import User
from app_factory import create_app
from datetime import datetime
app = create_app()

# Home route → login page
@app.route('/')
def home():
    return redirect(url_for('login'))

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(name=username).first()

        if user and check_password_hash(user.password, password):
            session['username'] = user.name
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

# Dashboard route (protected)
@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        user = User.query.filter_by(name=session['username']).first()
        return render_template('dashboard.html', user=user)
    else:
        flash('Please log in to continue.', 'warning')
        return redirect(url_for('login'))

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# Reset database route (use only in dev)
@app.route('/reset-db')
def reset_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
    return 'Database has been reset.'

# Placeholder: Filter by employee salary
@app.route('/employees/salary')
def filter_employees_by_salary():
    min_salary = request.args.get('min', type=float)
    return f"Employees with salary >= {min_salary}"

# Chrome DevTools support (optional for local debugging)
@app.route('/.well-known/appspecific/com.chrome.devtools.json')
def chrome_devtools_json():
    return '', 204



@app.context_processor
def inject_now():
    return {'now': datetime.now()}
