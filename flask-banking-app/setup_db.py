import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'user': 'postgres',
    'password': 'postgres',  # ✅ Updated password
    'database': 'bankdb'
}

def create_database():
    """Create the database if it doesn't exist"""
    try:
        # Connect to PostgreSQL server
        conn = psycopg2.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database='postgres'  # Connect to default db to create new db
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()

        # Check if database exists
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DB_CONFIG['database']}'")
        exists = cursor.fetchone()

        if not exists:
            cursor.execute(f"CREATE DATABASE {DB_CONFIG['database']}")
            print(f"✅ Database '{DB_CONFIG['database']}' created successfully!")
        else:
            print(f"ℹ️  Database '{DB_CONFIG['database']}' already exists.")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"❌ Error creating database: {e}")

def create_sample_data():
    """Create sample data for testing"""
    from app import app, db, User, Account, Transaction
    from werkzeug.security import generate_password_hash
    from decimal import Decimal
    import random

    with app.app_context():
        db.create_all()

        users_data = [
            {
                'username': 'john_doe',
                'email': 'john@example.com',
                'password': 'password123',
                'full_name': 'John Doe'
            },
            {
                'username': 'jane_smith',
                'email': 'jane@example.com',
                'password': 'password123',
                'full_name': 'Jane Smith'
            }
        ]

        for user_data in users_data:
            existing_user = User.query.filter_by(username=user_data['username']).first()
            if not existing_user:
                user = User(
                    username=user_data['username'],
                    email=user_data['email'],
                    password_hash=generate_password_hash(user_data['password']),
                    full_name=user_data['full_name']
                )
                db.session.add(user)
                db.session.commit()

                accounts_data = [
                    {'type': 'checking', 'balance': 5000.00},
                    {'type': 'savings', 'balance': 15000.00}
                ]

                for account_data in accounts_data:
                    account = Account(
                        account_number=f"ACC{random.randint(1000000000, 9999999999)}",
                        account_type=account_data['type'],
                        balance=Decimal(str(account_data['balance'])),
                        user_id=user.id
                    )
                    db.session.add(account)
                    db.session.commit()

                    transactions_data = [
                        {'type': 'deposit', 'amount': 1000.00, 'description': 'Initial deposit'},
                        {'type': 'withdrawal', 'amount': 200.00, 'description': 'ATM withdrawal'},
                        {'type': 'deposit', 'amount': 500.00, 'description': 'Salary deposit'},
                        {'type': 'withdrawal', 'amount': 150.00, 'description': 'Online purchase'}
                    ]

                    for trans_data in transactions_data:
                        transaction = Transaction(
                            transaction_type=trans_data['type'],
                            amount=Decimal(str(trans_data['amount'])),
                            description=trans_data['description'],
                            account_id=account.id
                        )
                        db.session.add(transaction)

                db.session.commit()
                print(f"✅ Sample data created for user: {user_data['username']}")

        print("🎉 Sample data creation completed!")

if __name__ == "__main__":
    print("🔧 Setting up database...")
    create_database()
    print("📥 Creating sample data...")
    create_sample_data()
    print("✅ Database setup completed!")
