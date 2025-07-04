from models.user_model import Base  # or db.Model
target_metadata = Base.metadata  # or db.metadata if using Flask-SQLAlchemy

