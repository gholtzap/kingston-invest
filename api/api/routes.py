from flask import Blueprint, request, send_file, jsonify
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from pymongo import MongoClient

from .alpha.alpha import calculate_decisions
from .beta.beta import generate_index_and_image
from .theta.register import register
from .theta.login import login
from .beta.save_index import save_user_index as core_save_index
from .beta.save_index import fetch_saved_indexes
from .theta.update_profile import update_user_profile


import json
import pandas as pd
import yfinance as yf
import os
import seaborn as sns
import matplotlib.dates as mdates
import matplotlib
matplotlib.use('Agg')

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/signup', methods=['POST'])
def backend_signup():
    return register()

@auth_bp.route('/login', methods = ['POST'])
def backend_login():
    return login()

tickers_bp = Blueprint('tickers_bp', __name__)

@tickers_bp.route('/alpha', methods=['POST'])
def tickers():
    data = request.json
    tickers = data.get('tickers')
    if not tickers:
        return {'error': 'No tickers provided'}, 400

    try:
        result = calculate_decisions(tickers)
        return {'result': result}
    except Exception as e:
        return {'error': str(e)}, 500

@tickers_bp.route('/beta', methods=['POST'])
def beta():
    data = request.json
    if not data:
        return {'error': 'No data provided'}, 400

    try:
        result = generate_index_and_image(data)
        return result, 200, {'ContentType': 'application/json'}
    except Exception as e:
        return {'error': str(e)}, 500
    
@tickers_bp.route('/saveIndex', methods=["POST"])
def save_index():
    data = request.json
    if not data:
        return {'error': 'No data provided'}, 400

    try:
        result = core_save_index(data)
        return result
 
    except Exception as e:
        return {'error': str(e)}, 500



@tickers_bp.route('/getSavedIndexes', methods=["GET"])
def get_saved_indexes_endpoint():
    username = request.args.get("username")
    if not username:
        return {'error': 'Username not provided'}, 400

    try:
        result = fetch_saved_indexes(username)
        return result
    except Exception as e:
        return {'error': str(e)}, 500



@auth_bp.route('/updateProfile', methods=['POST'])
def update_profile():
    # Assuming you have a method to authenticate the user and get their ID.
    user_id = request.form.get("userId")
    first_name = request.form.get("firstName")
    last_name = request.form.get("lastName")

    # Handle the profile picture upload
    profile_picture = None
    if 'profilePicture' in request.files:
        file = request.files['profilePicture']
        if file.filename != '':
            filename = secure_filename(file.filename)
            profile_picture = file.read()

    try:
        result = update_user_profile(user_id, first_name, last_name, profile_picture)
        return result
    except Exception as e:
        return {'error': str(e)}, 500
