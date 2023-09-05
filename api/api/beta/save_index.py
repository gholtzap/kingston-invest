from flask import Flask, jsonify, request
from pymongo import MongoClient
import os

MONGODB_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGODB_URI)
db = client["theta"] 
collection = db["custom-indexes"]  


def save_user_index(data):
    username = data.get("username")
    indexName = data.get("indexName")

    if not username or not indexName:
        return jsonify({"error": "Username or index name not provided"}), 400

    existing_data = collection.find_one({"username": username, "indexes.indexName": indexName})

    if existing_data:
        return jsonify({"error": "An index with this name already exists"}), 400

    collection.update_one(
        {"username": username},
        {
            "$push": {
                "indexes": {
                    "indexName": data.get("indexName"),
                    "tickers": data.get("tickers")
                }
            }
        },
        upsert=True
    )

    return jsonify({"message": "Index saved successfully"}), 200




def fetch_saved_indexes(username):
    user_data = collection.find_one({"username": username})

    if not user_data:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user_data.get("indexes", [])), 200

