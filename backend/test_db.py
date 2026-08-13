from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URL"))

try:
    client.admin.command("ping")
    print("✅ Connected to MongoDB Atlas!")
except Exception as e:
    print("❌ Connection Failed")
    print(e)
    