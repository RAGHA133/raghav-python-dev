from extensions import db
from app_factory import create_app
from models.user_model import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    db.create_all()
    existing_user = User.query.filter_by(email='admin@example.com').first()
    if not existing_user:
        admin = User(
            name='admin',
            email='admin@example.com',
            password=generate_password_hash('admin123'),
            account_type='admin',
            balance=1000.0
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin user seeded.")
    else:
        print("ℹ️ Admin user already exists. No changes made.")
