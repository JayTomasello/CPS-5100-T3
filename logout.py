from flask import Blueprint, redirect, url_for, request, make_response
from dbconfig import mydb

logout_bp = Blueprint('logout', __name__)

@logout_bp.route('/logout')
def logout():
    session_token = request.cookies.get('session_token')
    
    if session_token:
        # Clear the session token in your database
        mydb['User'].update_one({"session_token": session_token}, {"$set": {"session_token": None}})

    # Clear the session cookie in the response
    response = make_response(redirect(url_for('login.login')))
    response.set_cookie('session_token', '', expires=0)
    return response
