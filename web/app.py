from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

# Instantiate Flask api
app = Flask(__name__)
api = Api(app)

