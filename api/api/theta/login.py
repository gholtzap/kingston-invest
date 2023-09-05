from flask import Flask, request, jsonify
from werkzeug.security import check_password_hash
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

mongodb_uri = os.getenv('MONGODB_URI')
app = Flask(__name__)

client = MongoClient(mongodb_uri)
db = client['theta']
collection = db['accounts']

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = collection.find_one({'email': email})
    if user and check_password_hash(user['password'], password):
        return jsonify({'message': 'Login successful!', 'email': user['email'], 'username': user.get('username', 'Unknown')}), 200
    else:
        return jsonify({'error': 'Invalid email or password!'}), 400
