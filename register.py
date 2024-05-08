from flask import Blueprint, render_template, request, redirect, url_for
from dbconfig import mydb
import pymongo
import datetime
import hashlib

register_bp = Blueprint('register', __name__)

mycol = mydb['User']

# Function to hash the password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Route for registration form
@register_bp.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        # Get form inputs
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        # Validate form inputs
        if not name or not email or not password:
            error = "All fields are required."
        elif mycol.find_one({"u_email": email}):
            error = "Email address already exists."
        else:
            # Hash the password
            hashed_password = hash_password(password)

            # Insert user into the database
            user_data = {
                "name": name,
                "u_email": email,
                "password": hashed_password,
                "created": datetime.datetime.utcnow()
            }

            try:
                mycol.insert_one(user_data)
            except pymongo.errors.PyMongoError as e:
                error = f"An error occurred: {str(e)}"
            else:
                # Redirect user to a confirmation page
                return redirect(url_for('login.login'))

    # Render the registration form with error message, if any
    return render_template('register.html', error=error)
