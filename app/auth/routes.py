from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from app.auth.forms import LoginForm, RegisterForm
from app.auth.utils import send_confirmation_email, confirm_token, generate_confirmation_token
from app.server import db
from app.db.userauthmodel import User
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify

auth_routes = Blueprint("auth", __name__, template_folder="templates")

# @auth_routes.route("/login", methods=["GET", "POST"])
# def login():
#     form = LoginForm()
#
#     if form.validate_on_submit():
#         email = form.email.data.lower()
#         password = form.password.data
#
#         user = User.query.filter_by(email=email).first()
#
#         if not user or not check_password_hash(user.password, password):
#             flash("Invalid email or password", "danger")
#             return redirect(url_for("auth.login"))
#
#
#         login_user(user)
#         flash("Login successfull", "success")
#         return redirect(url_for("api.job_recommendations"))
#
#     return render_template("login.html", form=form)


# @auth_routes.route("/register", methods=["GET", "POST"])
# def register():
#     form = RegisterForm()  # Create a form instance
#
#     if form.validate_on_submit():
#         email = form.email.data
#         password = form.password.data
#
#         if User.query.filter_by(email=email).first():
#             flash("Email already registered. Please log in.", "warning")
#             return redirect(url_for("auth.login"))
#
#         user_data = {
#             "email": email,
#             "password": generate_password_hash(password)
#         }
#
#         token = generate_confirmation_token(user_data)
#
#         send_confirmation_email(email, token)
#
#         flash("A confirmation email has been sent. Please check your inbox.", "info")
#         return redirect(url_for("auth.login"))
#
#     return render_template('register.html', form=form)

@auth_routes.route("/login", methods=["POST"])
def login():
    # Get JSON data from the request
    data = request.get_json()

    # Validate input JSON
    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "Missing email or password"}), 400

    email = data["email"].lower()
    password = data["password"]

    user = User.query.filter_by(email=email).first()

    # Check if user exists and the password is correct
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid email or password"}), 401

    # Log in the user
    login_user(user)

    # Return a JSON response with a success message and a URL for job recommendations
    return jsonify({
        "message": "Login successful"
        # "redirect": url_for("api.job_recommendations", _external=True)
    }), 200

@auth_routes.route("/register", methods=["POST"])
def register():
    # Expect JSON input instead of a Flask form
    data = request.get_json()

    # Validate that both email and password are provided
    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "Missing email or password"}), 400

    email = data["email"]
    password = data["password"]

    # Logic remains the same: check if email is already registered
    if User.query.filter_by(email=email).first():
        # Instead of flashing and redirecting, return a JSON error message
        return jsonify({"warning": "Email already registered. Please log in."}), 409

    # Create the user_data dictionary with the hashed password
    user_data = {
        "email": email,
        "password": generate_password_hash(password)
    }

    # Generate a confirmation token using the same function
    token = generate_confirmation_token(user_data)

    # Send confirmation email as before
    send_confirmation_email(email, token)

    # Return a success JSON message (instead of flashing and redirecting)
    return jsonify({"info": "A confirmation email has been sent. Please check your inbox."}), 201

# @auth_routes.route("/confirm/<token>")
# def confirm_email(token):
#     user_data = confirm_token(token)
#     if not user_data:
#         flash("The confirmation link is invalid or has expired", "danger")
#         return redirect(url_for("auth.register"))
#
#     if User.query.filter_by(email=user_data["email"]).first():
#         flash("Account already confirmed. Please log in.", "success")
#         return redirect(url_for("auth.login"))
#
#
#     new_user = User(
#         email=user_data["email"],
#         password=user_data["password"],
#         confirmed=True)
#
#     db.session.add(new_user)
#     db.session.commit()
#
#     flash("Your account has been confirmed. You can login", "success")
#     return redirect(url_for("auth.login"))

@auth_routes.route("/confirm/<token>", methods=["GET"])
def confirm_email(token):
    user_data = confirm_token(token)
    if not user_data:
        # Instead of flashing and redirecting, return a JSON error
        return jsonify({"error": "The confirmation link is invalid or has expired"}), 400

    if User.query.filter_by(email=user_data["email"]).first():
        # Instead of redirecting, return a JSON message
        return jsonify({"message": "Account already confirmed. Please log in."}), 200

    new_user = User(
        email=user_data["email"],
        password=user_data["password"],
        confirmed=True
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Your account has been confirmed. You can login."}), 200

# @auth_routes.route("/logout")
# def logout():
#     logout_user()
#     flash("You have been logged out.", "info")
#     return redirect(url_for("auth.login"))

@auth_routes.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return jsonify({"info": "You have been logged out."}), 200
