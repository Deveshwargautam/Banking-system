from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Gautam",   # change if needed
    database="bankDB"
)

cursor = db.cursor()

# Home page
@app.route('/')
def home():
    return render_template('index.html')


# CREATE ACCOUNT
@app.route('/create', methods=['POST'])
def create_account():
    data = request.json
    try:
        cursor.execute(
            "INSERT INTO accounts VALUES (%s, %s, %s, %s)",
            (data['account_number'], data['name'], data['pin'], data['balance'])
        )
        db.commit()
        return jsonify({"message": "Account created successfully"})
    except Exception as e:
        return jsonify({"message": "Account already exists"})


# DEPOSIT
@app.route('/deposit', methods=['POST'])
def deposit():
    data = request.json

    cursor.execute("SELECT balance, pin FROM accounts WHERE account_number=%s",
                   (data['account_number'],))
    result = cursor.fetchone()

    if not result:
        return jsonify({"message": "Account not found"})

    balance, pin = result

    if pin != data['pin']:
        return jsonify({"message": "Invalid PIN"})

    new_balance = balance + data['amount']

    cursor.execute("UPDATE accounts SET balance=%s WHERE account_number=%s",
                   (new_balance, data['account_number']))
    db.commit()

    return jsonify({"message": "Deposit successful", "balance": new_balance})


# WITHDRAW
@app.route('/withdraw', methods=['POST'])
def withdraw():
    data = request.json

    cursor.execute("SELECT balance, pin FROM accounts WHERE account_number=%s",
                   (data['account_number'],))
    result = cursor.fetchone()

    if not result:
        return jsonify({"message": "Account not found"})

    balance, pin = result

    if pin != data['pin']:
        return jsonify({"message": "Invalid PIN"})

    if balance < data['amount']:
        return jsonify({"message": "Insufficient balance"})

    new_balance = balance - data['amount']

    cursor.execute("UPDATE accounts SET balance=%s WHERE account_number=%s",
                   (new_balance, data['account_number']))
    db.commit()

    return jsonify({"message": "Withdraw successful", "balance": new_balance})


# CHECK BALANCE
@app.route('/balance', methods=['POST'])
def check_balance():
    data = request.json

    cursor.execute("SELECT balance, pin FROM accounts WHERE account_number=%s",
                   (data['account_number'],))
    result = cursor.fetchone()

    if not result:
        return jsonify({"message": "Account not found"})

    balance, pin = result

    if pin != data['pin']:
        return jsonify({"message": "Invalid PIN"})

    return jsonify({"balance": balance})


if __name__ == '__main__':
    app.run(debug=True)