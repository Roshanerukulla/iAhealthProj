from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin

db = SQLAlchemy()
bcrypt = Bcrypt()

class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    def get_id(self):
        return str(self.id)
    def set_password(self, raw_password):
        self.password = bcrypt.generate_password_hash(raw_password).decode("utf-8")

    def check_password(self, raw_password):
        return bcrypt.check_password_hash(self.password, raw_password)
    
class UserProfile(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    preferred_name = db.Column(db.String(50))
    birth_date = db.Column(db.Date)
    gender = db.Column(db.Enum("Male", "Female", "Other"))

class UserPreferences(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    privacy_policies = db.Column(db.Enum("Yes", "No", "Maybe"))
    data_share = db.Column(db.Enum("Yes", "No", "Maybe"))
    searches = db.Column(db.Enum("Yes", "No", "Maybe"))
    answers = db.Column(db.Enum("Yes", "No", "Maybe"))
    storing = db.Column(db.Enum("Yes", "No", "Maybe"))

