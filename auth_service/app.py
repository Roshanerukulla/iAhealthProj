from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from models import db, bcrypt, Users
from routes import auth

app = Flask(__name__)
app.config.from_object(Config)

# Initialize the database
db.init_app(app)
bcrypt.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Define the user_loader function
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# Register Blueprint for authentication routes
app.register_blueprint(auth, url_prefix="/auth")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Creates the MySQL tables if they don't exist
    app.run(debug=True)
