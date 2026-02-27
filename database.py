from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")

if not MONGO_URL:
    raise ValueError("MONGO_URI not found in environment variables")

client = MongoClient(MONGO_URL)

db = client["financial_analyzer"]

users_collection = db["users"]
analysis_collection = db["analysis"]