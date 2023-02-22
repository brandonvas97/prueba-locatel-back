from flask import Flask, request, jsonify
import sqlite3
import random
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/', methods=['POST'])
def home():
    connection = sqlite3.connect('accounts.sql')
    cur = connection.cursor()
    content = request.json
    number_account = content['number_account']
    password = content['password']
    if number_account == "" or password == "" or number_account is None or password is None:
        return jsonify({"response":f"Llenar todos los campos"})
    query = f"SELECT * FROM accounts WHERE number_account = {number_account} and password = '{password}'"
    elements = cur.execute(query).fetchall()
    if len(elements) > 0:
        balance = elements[0][4]
        account_balance_result_str = f'{balance:,}'
        parsed = account_balance_result_str.replace(',', '.')
        connection.close()
        return jsonify({"response":f"Balance actual: {parsed}"})
    else:
        connection.close()
        return jsonify({"response":f"Cuenta no encontrada o contraseña incorrecta"})


@app.route('/crear', methods=['POST'])
def create():
    content = request.json
    client_name = content['client_name']
    password = content['password']
    if client_name == "" or password == "" or client_name is None or password is None:
        return jsonify({"response":f"Llenar todos los campos"})
    connection = sqlite3.connect('accounts.sql')
    cur = connection.cursor()
    i=0
    account_number_str = ""
    while i <= 10:
        number = str(random.randrange(0,9))
        account_number_str += number
        i+=1
    account_number = int(account_number_str)
    #print(account_number)
    query = f"INSERT INTO accounts (number_account, client_name, password, balance) VALUES ({account_number}, '{client_name}', '{password}', 0)"
    res = cur.execute(query).fetchall()
    connection.commit()
    #print(res) #devuelve [] de ser correcto
    connection.close()
    return jsonify({"response":f"Cuenta creada exitosamente con el número: {account_number}"})

@app.route('/consignar', methods=['POST'])
def consignar():
    content = request.json
    connection = sqlite3.connect('accounts.sql')
    cur = connection.cursor()
    number_account = content['number_account']
    value = content['value']
    if number_account == "" or value =="" or value is None or number_account is None:
        return jsonify({"response":f"Llenar todos los campos"})
    query = f"SELECT * FROM accounts WHERE number_account = {number_account}"
    elements = cur.execute(query).fetchall()
    if len(elements) > 0:
        account_balance = elements[0][4]
        value = content['value']
        account_balance += value
        query2 = f"UPDATE accounts SET balance = {account_balance} WHERE number_account = {number_account}"
        res = cur.execute(query2).fetchall()
        connection.commit()
        connection.close()
        return jsonify({"response":f"Consignación exitosa"})
    else:
        connection.close()
        return jsonify({"response":f"Cuenta no encontrada"})

@app.route('/retirar', methods=['POST'])
def retirar():
    content = request.json
    connection = sqlite3.connect('accounts.sql')
    cur = connection.cursor()
    number_account = content['number_account']
    password = content['password']
    value = content['value']
    if number_account == "" or password == "" or value == "" or value is None or number_account is None or password is None:
        return jsonify({"response":f"Llenar todos los campos"})
    query = f"SELECT * FROM accounts WHERE number_account = {number_account} and password = '{password}'"
    elements = cur.execute(query).fetchall()
    if len(elements) > 0:
        account_balance = elements[0][4]
        value = content['value']
        account_balance_result = account_balance - value
        if account_balance_result < 0:
            connection.close()
            account_balance_result_str = f'{account_balance:,}'
            parsed = account_balance_result_str.replace(',', '.')
            return jsonify({"response":f"Saldo insuficiente, balance actual: {parsed}"})
        query2 = f"UPDATE accounts SET balance = {account_balance_result} WHERE number_account = {number_account}"
        res = cur.execute(query2).fetchall()
        account_balance_result_str = f'{account_balance_result:,}'
        parsed = account_balance_result_str.replace(',', '.')
        connection.commit()
        connection.close()
        return jsonify({"response":f"Retiro exitoso, balance actual: {parsed}"})
    else:
        connection.close()
        return jsonify({"response":f"Cuenta no encontrada o contraseña incorrecta"})

if (__name__ == '__main__'):
    app.run()
