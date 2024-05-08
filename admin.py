from flask import Blueprint, render_template, request, redirect, url_for
from dbconfig import mydb

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dispute_management')
def dispute_management():
    session_token = request.cookies.get('session_token')
    user = mydb['User'].find_one({"session_token": session_token})
    
    if user and user['u_email'].endswith('@admin.edu'):
        # Fetch all disputes with status "Disputed" from the database
        disputes = list(mydb['Favor'].find({"status": "Disputed"}))

        # Transforming the data to be more template-friendly
        for dispute in disputes:
            dispute['_id'] = str(dispute['_id'])  # Converting ObjectId to string for use in the template

        return render_template('dispute_management.html', disputes=disputes)
    else:
        # Redirect to login if not authenticated or not an admin
        return redirect(url_for('login.login'))
