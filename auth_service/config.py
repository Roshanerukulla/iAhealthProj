import urllib.parse
import os 

class Config:
    SECRET_KEY = 'your_secret_key'
    password = "Gupta@4k4"
    encoded_password = urllib.parse.quote_plus(password)
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:{encoded_password}@localhost/auth_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")  # For session management
