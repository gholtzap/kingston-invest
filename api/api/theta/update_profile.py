from pymongo import MongoClient
from dotenv import load_dotenv
from bson import ObjectId
import os

load_dotenv()

mongodb_uri = os.getenv('MONGODB_URI')
if not mongodb_uri:
    raise ValueError("MONGODB_URI is not set in the environment variables.")
client = MongoClient(mongodb_uri)
db = client.theta
accounts_collection = db.accounts

def update_user_profile(user_id, first_name, last_name, profile_picture):
    try:
        account_query = {"_id": ObjectId(user_id)}
        
        update_data = {}
        if first_name:
            update_data["firstName"] = first_name
        if last_name:
            update_data["lastName"] = last_name
        if profile_picture:
            update_data["profilePicture"] = profile_picture
        
        accounts_collection.update_one(account_query, {"$set": update_data})

        return {"message": "Profile updated successfully"}, 200
    except Exception as e:
        return {"error": str(e)}, 500
