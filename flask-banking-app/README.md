# SecureBank - Flask Banking Application

A complete banking application built with Flask, featuring user authentication, account management, and transaction processing with PostgreSQL database integration.

## Features

- **User Authentication**: Secure login/registration with JWT tokens
- **Account Management**: Multiple account types (Checking, Savings)
- **Transaction Processing**: Deposits, withdrawals, and transfers
- **Dashboard**: Real-time KPIs and account overview
- **Security**: Password hashing, JWT authentication, and secure cookies
- **Responsive UI**: Bootstrap-based interface with modern design

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: PostgreSQL
- **Authentication**: JWT tokens with secure cookies
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **ORM**: SQLAlchemy
- **Charts**: Chart.js for data visualization

## Installation

### Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd flask-banking-app
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure PostgreSQL**
   - Install PostgreSQL
   - Create a database named `bankdb`
   - Update database credentials in `.env` file

5. **Environment Configuration**
   - Copy `.env.example` to `.env`
   - Update database credentials and secret keys:
   ```
   DATABASE_URL=postgresql://your_username:your_password@localhost/bankdb
   SECRET_KEY=your-secret-key-here
   JWT_SECRET_KEY=your-jwt-secret-here
   ```

6. **Initialize Database**
   ```bash
   python setup_db.py
   ```

7. **Run the application**
   ```bash
   python app.py
   ```

8. **Access the application**
   - Open browser and go to `http://localhost:5000`
   - Use sample credentials:
     - Username: `john_doe` or `jane_smith`
     - Password: `password123`

## File Structure

```
flask-banking-app/
├── app.py                 # Main Flask application
├── setup_db.py           # Database setup script
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables
├── README.md             # This file
└── templates/            # HTML templates
    ├── base.html         # Base template
    ├── login.html        # Login page
    ├── register.html     # Registration page
    ├── dashboard.html    # Main dashboard
    ├── transfer.html     # Money transfer page
    └── account_details.html  # Account details
```

## Database Schema

### Users Table
- `id`: Primary key
- `username`: Unique username
- `email`: User email
- `password_hash`: Hashed password
- `full_name`: User's full name
- `created_at`: Registration timestamp

### Accounts Table
- `id`: Primary key
- `account_number`: Unique account number
- `account_type`: checking/savings
- `balance`: Account balance
- `user_id`: Foreign key to users
- `created_at`: Account creation timestamp

### Transactions Table
- `id`: Primary key
- `transaction_type`: deposit/withdrawal/transfer
- `amount`: Transaction amount
- `description`: Transaction description
- `account_id`: Foreign key to accounts
- `created_at`: Transaction timestamp

## API Endpoints

### Authentication
- `POST /login` - User login
- `POST /register` - User registration
- `GET /logout` - User logout

### Dashboard
- `GET /dashboard` - Main dashboard
- `GET /api/kpis` - KPIs JSON API

### Account Management
- `GET /account/<id>` - Account details
- `POST /transfer` - Money transfer

## Security Features

- **Password Hashing**: Using Werkzeug's security functions
- **JWT Authentication**: Secure token-based authentication
- **Secure Cookies**: HTTP-only cookies for token storage
- **SQL Injection Prevention**: SQLAlchemy ORM protection
- **CSRF Protection**: Built-in Flask security

## Key Performance Indicators (KPIs)

- Total account balance
- Number of active accounts
- Monthly deposits/withdrawals
- Transaction history
- Account balance distribution

## Usage

1. **Registration**: Create a new account with username, email, and password
2. **Login**: Authenticate with credentials
3. **Dashboard**: View account overview and KPIs
4. **Transfer Money**: Send money between accounts
5. **Account Details**: View transaction history

## Development

### Running in Development Mode
```bash
export FLASK_ENV=development
flask run --debug
```

### Database Migrations
```bash
# If you make changes to models, recreate the database
python setup_db.py
```

### Adding New Features
1. Update models in `app.py`
2. Create new routes
3. Add corresponding HTML templates
4. Update navigation in `base.html`

## Production Deployment

1. **Environment Variables**: Set production values for secret keys
2. **Database**: Use production PostgreSQL instance
3. **Security**: Enable HTTPS, set secure cookie flags
4. **Monitoring**: Add logging and monitoring
5. **Backup**: Implement database backup strategy

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions, please create an issue in the repository.