# Required packages
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Environment variables
load_dotenv()
MONGO_URI = os.getenv('MONGO_URI')

# Set up connection with MongoDB
client = MongoClient(MONGO_URI)

# Create a new Mongo database
db = client['MealOn']

# Create required collections in the database
users = db['users']
orders = db['orders']
menu = db['menu']