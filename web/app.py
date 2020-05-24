from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

# Instantiate Flask api
app = Flask(__name__)
api = Api(app)

# Connect to the MongoDB client on default port
client = MongoClient('mongodb://db:27017')

# Define new database
db = client.BankAPI
users = db['Users']

# Check if user exists in database
def UserExist(username):
    # Find query username in MongoDB
    if users.find({'Username': username}).count() == 0:
        return False
    else:
        return True

