import logging
from flask import Flask, render_template, request, redirect, url_for, flash, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from functools import wraps
from decimal import Decimal
import random

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/bankdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string-change-this-in-production'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

# Initialize DB
db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    full_name = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    accounts = db.relationship('Account', backref='user', lazy=True)

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.String(20), unique=True, nullable=False)
    account_type = db.Column(db.String(20), nullable=False)
    balance = db.Column(db.Numeric(15, 2), default=0.00)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    transactions = db.relationship('Transaction', backref='account', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'account_number': self.account_number,
            'account_type': self.account_type,
            'balance': float(self.balance),
            'created_at': self.created_at.strftime('%Y-%m-%d'),
            'is_active': self.is_active
        }

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction_type = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Numeric(15, 2), nullable=False)
    description = db.Column(db.String(200))
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='completed')

# JWT utilities
def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + app.config['JWT_ACCESS_TOKEN_EXPIRES']
    }
    token = jwt.encode(payload, app.config['JWT_SECRET_KEY'], algorithm='HS256')
    logger.info(f"Generated JWT token for user_id={user_id}")
    return token

def verify_token(token):
    try:
        payload = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        logger.info(f"JWT token verified for user_id={payload['user_id']}")
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        logger.warning("JWT token expired")
        return None
    except jwt.InvalidTokenError:
        logger.error("Invalid JWT token")
        return None

# Decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('token')
        if not token:
            logger.warning("Missing JWT token in request")
            return redirect(url_for('login'))
        user_id = verify_token(token)
        if not user_id:
            logger.warning("JWT verification failed")
            return redirect(url_for('login'))
        current_user = db.session.get(User, user_id)
        if not current_user:
            logger.warning(f"User not found for user_id: {user_id}")
            return redirect(url_for('login'))
        logger.info(f"User {current_user.username} accessed {request.path}")
        return f(current_user, *args, **kwargs)
    return decorated

# Routes
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            token = generate_token(user.id)
            response = make_response(redirect(url_for('dashboard')))
            response.set_cookie('token', token, max_age=3600)
            logger.info(f"User '{username}' logged in successfully")
            return response
        else:
            logger.warning(f"Failed login attempt for username: {username}")
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        full_name = request.form.get('full_name')

        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            logger.warning(f"Attempted registration with existing username: {username}")
            return render_template('register.html')

        if User.query.filter_by(email=email).first():
            flash('Email already exists')
            logger.warning(f"Attempted registration with existing email: {email}")
            return render_template('register.html')

        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            full_name=full_name
        )
        db.session.add(user)
        db.session.commit()
        logger.info(f"User registered: {username}")

        account_number = f"ACC{random.randint(1000000000, 9999999999)}"
        account = Account(
            account_number=account_number,
            account_type='checking',
            balance=Decimal('1000.00'),
            user_id=user.id
        )
        db.session.add(account)
        db.session.commit()
        logger.info(f"Default account created for user '{username}' - {account_number}")

        flash('Registration successful! You can now login.')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/dashboard')
@token_required
def dashboard(current_user):
    account_objs = Account.query.filter_by(user_id=current_user.id, is_active=True).all()
    accounts = [acc.to_dict() for acc in account_objs]
    total_balance = sum(acc['balance'] for acc in accounts)
    total_accounts = len(accounts)

    recent_transactions = Transaction.query.join(Account).filter(
        Account.user_id == current_user.id
    ).order_by(Transaction.created_at.desc()).limit(5).all()

    monthly_deposits = db.session.query(db.func.sum(Transaction.amount)).join(Account).filter(
        Account.user_id == current_user.id,
        Transaction.transaction_type == 'deposit',
        Transaction.created_at >= datetime.utcnow() - timedelta(days=30)
    ).scalar() or 0

    monthly_withdrawals = db.session.query(db.func.sum(Transaction.amount)).join(Account).filter(
        Account.user_id == current_user.id,
        Transaction.transaction_type == 'withdrawal',
        Transaction.created_at >= datetime.utcnow() - timedelta(days=30)
    ).scalar() or 0

    return render_template('dashboard.html',
                           user=current_user,
                           accounts=accounts,
                           total_balance=total_balance,
                           total_accounts=total_accounts,
                           recent_transactions=recent_transactions,
                           monthly_deposits=float(monthly_deposits),
                           monthly_withdrawals=float(monthly_withdrawals))

@app.route('/account/<int:account_id>')
@token_required
def account_details(current_user, account_id):
    account = Account.query.filter_by(id=account_id, user_id=current_user.id).first()
    if not account:
        flash('Account not found')
        logger.warning(f"User {current_user.username} tried accessing non-existent account ID: {account_id}")
        return redirect(url_for('dashboard'))
    transactions = Transaction.query.filter_by(account_id=account.id).order_by(
        Transaction.created_at.desc()
    ).all()
    return render_template('account_details.html', account=account, transactions=transactions)

@app.route('/transfer', methods=['GET', 'POST'])
@token_required
def transfer(current_user):
    if request.method == 'POST':
        from_account_id = request.form.get('from_account')
        to_account_number = request.form.get('to_account')
        amount = float(request.form.get('amount'))
        description = request.form.get('description', '')

        from_account = Account.query.filter_by(id=from_account_id, user_id=current_user.id).first()
        to_account = Account.query.filter_by(account_number=to_account_number).first()

        if not from_account or not to_account:
            flash('Invalid account details')
            logger.warning(f"Transfer failed: Invalid account (from: {from_account_id}, to: {to_account_number})")
            return redirect(url_for('transfer'))

        if float(from_account.balance) < amount:
            flash('Insufficient funds')
            logger.warning(f"Transfer failed: Insufficient funds in account {from_account.account_number}")
            return redirect(url_for('transfer'))

        from_account.balance -= Decimal(str(amount))
        to_account.balance += Decimal(str(amount))

        db.session.add(Transaction(
            transaction_type='withdrawal',
            amount=Decimal(str(amount)),
            description=f'Transfer to {to_account.account_number}: {description}',
            account_id=from_account.id
        ))
        db.session.add(Transaction(
            transaction_type='deposit',
            amount=Decimal(str(amount)),
            description=f'Transfer from {from_account.account_number}: {description}',
            account_id=to_account.id
        ))

        db.session.commit()
        logger.info(f"Transfer of {amount} from {from_account.account_number} to {to_account.account_number}")
        flash('Transfer completed successfully')
        return redirect(url_for('dashboard'))

    account_objs = Account.query.filter_by(user_id=current_user.id, is_active=True).all()
    return render_template('transfer.html', accounts=account_objs)

@app.route('/api/kpis')
@token_required
def api_kpis(current_user):
    account_objs = Account.query.filter_by(user_id=current_user.id, is_active=True).all()
    return jsonify({
        'total_balance': float(sum(acc.balance for acc in account_objs)),
        'total_accounts': len(account_objs),
        'account_breakdown': [acc.to_dict() for acc in account_objs]
    })

@app.route('/logout')
def logout():
    token = request.cookies.get('token')
    user_id = verify_token(token) if token else None
    logger.info(f"User {user_id} logged out")
    response = make_response(redirect(url_for('login')))
    response.set_cookie('token', '', expires=0)
    return response

# Entry point
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
