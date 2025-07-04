from app import db
from models.user_model import User

user = User(username='ragh.p', password='yourpassword123', email='ragh.p@cgi.com', full_name='Raghav P')
db.session.add(user)
db.session.commit()

print("Test user created.")

