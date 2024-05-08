from flask import Blueprint, render_template, request, redirect, url_for, make_response
import pymongo
import hashlib
import os
import binascii
from dbconfig import mydb

login_bp = Blueprint('login', __name__)
mycol = mydb["User"]

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generate_session_token():
    return binascii.hexlify(os.urandom(24)).decode()

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        hashed_password = hash_password(password)
        user = mycol.find_one({"u_email": email, "password": hashed_password})

        if user:
            email_domain = email.split('@')[1]  # Extract the domain from the email
            if email_domain == 'admin.edu':
                # Admin login logic
                session_token = generate_session_token() + str(user['_id'])
                mycol.update_one({"_id": user['_id']}, {"$set": {"session_token": session_token}})
                response = make_response(redirect(url_for('admin.dispute_management')))
            else:
                # Regular user login logic
                session_token = generate_session_token() + str(user['_id'])
                mycol.update_one({"_id": user['_id']}, {"$set": {"session_token": session_token}})
                response = make_response(redirect(url_for('homepage.homepage')))
                
            response.set_cookie('session_token', session_token, httponly=True, secure=True)
            return response
        else:
            error = "Invalid email or password. Please try again."

    return render_template('login.html', error=error)


