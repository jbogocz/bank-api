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

# Register new user, inherit class from Resource
class Register(Resource):
    # define POST
    def post(self):
        # json from POST
        postedData = request.get_json()
        # get username & pass
        username = postedData['username']
        password = postedData['password']
        # Check if user already exists
        if UserExist(username):
            # if True set 301 status
            retJson = {
                'status': 301,
                'msg': 'Invalid Username'
            }
            return jsonify(retJson)

        # otherwise, if user not exists than get & hash password
        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        # store user hashed password in database
        users.insert({
            'Username': username,
            'Password': hashed_pw,
            # add own money & debt of user
            'Own': 0,
            'Debt': 0
        })
        # return json to the user
        retJson = {
            'status': 200,
            'msg': 'You successfully signed up for this API'
        }
        return jsonify(retJson)

# Verify user hashed password
def verify_pw(username, password):
    # Check if user exists
    if not UserExist(username):
        return False
    # get hashed pass
    hashed_pw = users.find({
        'Username': username
    })[0]['Password']
    # match hashed passwords user provide vs stored in mongodb
    if bcrypt.hashpw(password.endcode('utf8'), hashed_pw) == hashed_pw:
        return True
    else:
        return False

# Check user cash amount
def cashWithUser(username):
    cash = users.find({
        "Username": username
    })[0]["Own"]
    return cash

# Check user debt
def debtWithUser(username):
    debt = users.find({
        "Username": username
    })[0]["Debt"]
    return debt

# Generate dictionary for user
def generateReturnDictionary(status, msg):
    retJson = {
        'status': status,
        'msg': msg
    }
    return retJson

# Check user credentials
def verifyCredentials(username, password):
    # Check if user exists
    if not UserExist(username):
        return generateReturnDictionary(301, 'Invalid Username'), True
    # Check if password is valid
    correct_pw = verify_pw(username, password)
    if not correct_pw:
        return generateReturnDictionary(302, 'Invalid Password'), True
    return None, False

# Update user account balance
def updateAccount(username, balance):
    users.update({
        "Username": username
    }, {
        "$set": {
            "Own": balance
        }
    })

# Update user debt balance
def updateDebt(username, balance):
    users.update({
        "Username": username
    }, {
        "$set": {
            "Debt": balance
        }
    })

# Add money to user account
class Add(Resource):
    def post(self):
        postedData = request.get_json()
        # Get POSTed data
        username = postedData["username"]
        password = postedData["password"]
        money = postedData["amount"]
        # Verify credentials
        retJson, error = verifyCredentials(username, password)
        if error:
            return jsonify(retJson)
        # Check amout of cash
        if money <= 0:
            return jsonify(generateReturnDictionary(304, "The money amount entered must be greater than 0"))
        # Check user cash amout
        cash = cashWithUser(username)
        money -= 1  # Transaction fee
        # Add transaction fee to bank account
        bank_cash = cashWithUser("BANK")
        updateAccount("BANK", bank_cash+1)
        # Add remaining to user
        updateAccount(username, cash+money)

        return jsonify(generateReturnDictionary(200, "Amount Added Successfully to account"))

# Transfer money between users
class Transfer(Resource):
    def post(self):
        postedData = request.get_json()
        # Get POSTed data
        username = postedData["username"]
        password = postedData["password"]
        to = postedData["to"]
        money = postedData["amount"]
        # Verify credentials
        retJson, error = verifyCredentials(username, password)
        if error:
            return jsonify(retJson)
        # Check if amout of cash is enough for transfer
        cash = cashWithUser(username)
        if cash <= 0:
            return jsonify(generateReturnDictionary(303, "You are out of money, please Add Cash or take a loan"))
        if money <= 0:
            return jsonify(generateReturnDictionary(304, "The money amount entered must be greater than 0"))
        if not UserExist(to):
            return jsonify(generateReturnDictionary(301, "Recieved username is invalid"))
        # Get balance from user, receiver & bank
        cash_from = cashWithUser(username)
        cash_to = cashWithUser(to)
        bank_cash = cashWithUser("BANK")
        # Update balance of user, receiver & bank
        updateAccount("BANK", bank_cash+1)
        updateAccount(to, cash_to+money-1)
        updateAccount(username, cash_from - money)

        retJson = {
            "status": 200,
            "msg": "Amount added successfully to account"
        }
        return jsonify(generateReturnDictionary(200, "Amount added successfully to account"))

# Check user account balance
class Balance(Resource):
    def post(self):
        postedData = request.get_json()
        # Get POSTed data
        username = postedData["username"]
        password = postedData["password"]
        # Verify credentials
        retJson, error = verifyCredentials(username, password)
        if error:
            return jsonify(retJson)
        # Return json file & emit user id and pass
        retJson = users.find({
            "Username": username
        }, {
            "Password": 0,  # projection
            "_id": 0
        })[0]

        return jsonify(retJson)

# Add load to the user account
class TakeLoan(Resource):
    def post(self):
        postedData = request.get_json()
        # Get POSTed data
        username = postedData["username"]
        password = postedData["password"]
        money = postedData["amount"]
        # Verify credentials
        retJson, error = verifyCredentials(username, password)
        if error:
            return jsonify(retJson)
        # check user cash, debt and update user cash and increase debt
        cash = cashWithUser(username)
        debt = debtWithUser(username)
        updateAccount(username, cash + money)
        updateDebt(username, debt + money)

        return jsonify(generateReturnDictionary(200, "Loan Added to Your Account"))

# Pay load, substract from user account
class PayLoan(Resource):
    def post(self):
        postedData = request.get_json()
        # Get POSTed data
        username = postedData["username"]
        password = postedData["password"]
        money = postedData["amount"]
        # Verify credentials
        retJson, error = verifyCredentials(username, password)
        if error:
            return jsonify(retJson)
        # check user cash
        cash = cashWithUser(username)
        if cash < money:
            return jsonify(generateReturnDictionary(303, "Not Enough Cash in your account"))
        else:
            debt = debtWithUser(username)
            updateAccount(username, cash - money)
            updateDebt(username, debt - money)

        return jsonify(generateReturnDictionary(200, "Loan Paid"))

# Add resources to the API
api.add_resource(Register, '/register')
api.add_resource(Add, '/add')
api.add_resource(Transfer, '/transfer')
api.add_resource(Balance, '/balance')
api.add_resource(TakeLoan, '/takeloan')
api.add_resource(PayLoan, '/payloan')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
