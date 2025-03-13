from flask import Blueprint, request, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from models import db, Users, UserProfile, UserPreferences
from flask_bcrypt import Bcrypt

# Initialize Bcrypt and Blueprint
bcrypt = Bcrypt()
auth = Blueprint("auth", __name__)

# ---------------------- ROUTES ------------------------

# 1️⃣ Register New User
@auth.route("/register", methods=["POST"])
def register():
    data = request.json
    email = data["email"]
    password = data["password"]
    confirm_password = data["confirm_password"]

    if password != confirm_password:
        return jsonify({"error": "Passwords do not match"}), 400

    # Check if email already exists
    existing_user = Users.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "Email already registered"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    new_user = Users(email=email, password=hashed_password)
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "User registered successfully!"}), 201


# 2️⃣ User Login
@auth.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data["email"]
    password = data["password"]

    user = Users.query.filter_by(email=email).first()

    if user and bcrypt.check_password_hash(user.password, password):
        login_user(user)
        return jsonify({"message": "Login successful!"})
    
    return jsonify({"error": "Invalid credentials"}), 401


# Enter Basic Information (After Login)
@auth.route("/profile", methods=["POST"])
@login_required
def update_profile():
    data = request.json

    profile = UserProfile(
        user_id=current_user.id,
        first_name=data["first_name"],
        last_name=data["last_name"],
        preferred_name=data["preferred_name"],
        birth_date=data["birth_date"],
        gender=data["gender"]
    )

    db.session.add(profile)
    db.session.commit()

    return jsonify({"message": "Profile updated successfully!"})


# 4️⃣ Enter Preferences
@auth.route("/preferences", methods=["POST"])
@login_required
def update_preferences():
    data = request.json

    preferences = UserPreferences(
        user_id=current_user.id,
        privacy_policies=data["privacy_policies"],
        data_share=data["data_share"],
        searches=data["searches"],
        answers=data["answers"],
        storing=data["storing"]
    )

    db.session.add(preferences)
    db.session.commit()

    return jsonify({"message": "Preferences saved successfully!"})


# 5️⃣ Logout
@auth.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully!"})


# Register routes in the main app
def register_routes(app):
    app.register_blueprint(auth, url_prefix="/auth")
