from flask import Blueprint, request, send_file, jsonify
from werkzeug.security import generate_password_hash
from pymongo import MongoClient

from .alpha import calculate_decisions
from .beta import generate_index_and_image
from .theta.register import register
from .theta.login import login

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
