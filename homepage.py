from flask import Blueprint, render_template, jsonify, request, redirect, url_for, session
import datetime
import pymongo
from bson import ObjectId
from dbconfig import mydb

homepage_bp = Blueprint('homepage', __name__)

def get_user_id_from_session(token):
    user = mydb['User'].find_one({"session_token": token})
    return str(user['_id']) if user else None

@homepage_bp.route('/homepage', methods=['GET'])
def homepage():
    session_token = request.cookies.get('session_token')
    if not session_token or not get_user_id_from_session(session_token):
        return redirect(url_for('login.login'))
    user_id = get_user_id_from_session(session_token)
    return render_template('homepage.html', now=datetime.datetime.utcnow().isoformat())

@homepage_bp.route('/create_favor', methods=['POST'])
def create_favor():
    data = request.get_json()
    session_token = request.cookies.get('session_token')
    user_id = get_user_id_from_session(session_token)
    if not user_id:
        return jsonify({'status': 'error', 'message': 'User not authenticated'}), 401

    try:
        deadline = datetime.datetime.strptime(data['deadline'], '%Y-%m-%dT%H:%M')
        if deadline <= datetime.datetime.utcnow():
            return jsonify({'status': 'error', 'message': 'Deadline must be in the future'}), 400

        favor = {
            "requester_id": ObjectId(user_id),
            "title": data['title'],
            "description": data['description'],
            "monetary_value": float(data['monetary_value']),
            "deadline": deadline,
            "category": data['category'],
            "status": "Created",
            "pick_up_location": data['pick_up_location'],
            "drop_off_location": data['drop_off_location'],
            "payment_type": data['payment_type'],
            "proposals": [],
            "created": datetime.datetime.utcnow()
        }

        mydb['Favor'].insert_one(favor)
        return jsonify({'status': 'success', 'message': 'Favor created successfully'})
    except pymongo.errors.PyMongoError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@homepage_bp.route('/get_favors/<filter_type>', methods=['GET'])
def get_favors(filter_type):
    session_token = request.cookies.get('session_token')
    user_id = get_user_id_from_session(session_token) if session_token else None
    query = {}

    if filter_type == 'complete':
        query['status'] = 'Complete'
    elif filter_type == 'incomplete':
        query['status'] = 'Accepted'
    elif filter_type == 'created':
        query = {'$and': [{'requester_id': ObjectId(user_id)}, {'status': 'Created'}]}
    elif filter_type == 'all':
        query['status'] = 'Created'  # Only show created statuses in all favors
    else:
        query = {}  # Fetch all favors if no specific filter is applied

    favors = list(mydb['Favor'].find(query))
    for favor in favors:
        favor['_id'] = str(favor['_id'])
        favor['requester_id'] = str(favor['requester_id'])
        favor['deadline'] = favor['deadline'].isoformat()
        if 'proposals' in favor:
            favor['proposals'] = [{**p, 'requestee_id': str(p['requestee_id'])} for p in favor['proposals']]
    return jsonify(favors)


@homepage_bp.route('/accept_proposal/<favor_id>', methods=['POST'])
def accept_proposal(favor_id):
    mydb['Favor'].update_one(
        {'_id': ObjectId(favor_id)},
        {'$set': {'status': 'Accepted'}}
    )
    return jsonify({'status': 'success', 'message': 'Favor accepted successfully'})

@homepage_bp.route('/delete_favor/<favor_id>', methods=['POST'])
def delete_favor(favor_id):
    mydb['Favor'].delete_one({'_id': ObjectId(favor_id)})
    return jsonify({'status': 'success', 'message': 'Favor deleted successfully'})

@homepage_bp.route('/change_favor_status/<favor_id>', methods=['POST'])
def change_favor_status(favor_id):
    data = request.get_json()
    new_status = data.get('status')
    mydb['Favor'].update_one(
        {'_id': ObjectId(favor_id)},
        {'$set': {'status': new_status}}
    )
    return jsonify({'status': 'success', 'message': 'Favor status updated to ' + new_status})

@homepage_bp.route('/favor_detail/<favor_id>', methods=['GET'])
def favor_detail(favor_id):
    favor = mydb['Favor'].find_one({'_id': ObjectId(favor_id)})
    if not favor:
        return "Favor not found", 404
    return render_template('favor_detail.html', favor=favor)

@homepage_bp.route('/custom_filters', methods=['POST'])
def custom_filters():
    data = request.get_json()
    category = data.get('category', '')
    monetaryValue = data.get('monetaryValue', 0)

    query = {}
    if category:
        query["category"] = category
    if monetaryValue:
        query["monetary_value"] = {"$gte": float(monetaryValue)}

    favors = list(mydb['Favor'].find(query))
    for favor in favors:
        favor['_id'] = str(favor['_id'])
        favor['requester_id'] = str(favor['requester_id'])
        favor['deadline'] = favor['deadline'].isoformat()

    return jsonify(favors)
