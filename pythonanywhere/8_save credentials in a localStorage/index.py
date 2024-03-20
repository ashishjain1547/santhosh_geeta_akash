from flask import Flask, redirect, render_template, request, url_for, make_response

import json, requests

from flask_cors import CORS, cross_origin

from flask import Response, jsonify

import jwt
import datetime

from functools import wraps
import sqlite3

app=Flask(__name__)
app.config['SECRET_KEY'] = 'Alpha'

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
def welcome():
    #return render_template("index.html")
    return "Welcome to questionnaire app!"




@app.route("/submit_using_jquery", methods=["POST"])
@cross_origin()
def submit_using_jquery():
    
    username = request.form["username"]
    password = request.form["password"]
    confirm_password = request.form["confirm_password"]
    
    if username != "" and password == confirm_password: 

        conn = sqlite3.connect('questionnaire.db')

        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()

        print('Opened database successfully')
        #print(request.form)

        # Creating table
        table = """CREATE TABLE IF NOT EXISTS USER_LOGIN 
        (
            username TEXT NOT NULL UNIQUE, 
            password TEXT NOT NULL
        ) """

        cursor.execute(table)

        # Queries to INSERT records.
        try:
            cursor.execute("INSERT INTO USER_LOGIN (username, password) VALUES (?, ?)", (username, password))
        except sqlite3.IntegrityError as e:
            return make_response('Username is not unique', 4001)
        
        conn.commit()
        conn.close()
        
        # In a real scenario, password should be securely hashed
        token = jwt.encode({'user': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1)}, app.config['SECRET_KEY'])

        # Original ChatGPT code
        # return jsonify({'token': token.decode('UTF-8')})
        return jsonify({ 
            'username': username,
            'token': token 
        })

    return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


# Decorator to check if the user is logged in (JWT token is present and valid)
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            print("from token_required: " + str(data))
        except Exception as e:
            print(e)
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(*args, **kwargs)

    return decorated


@app.route('/show_all_questions')
@cross_origin()
@token_required
def show_all_questions():

    connection = sqlite3.connect('questionnaire.db')
    cursor = connection.cursor()

    # Fetch column names
    cursor.execute(f"PRAGMA table_info(question_bank)")
    columns = [column[1] for column in cursor.fetchall()]

    # Fetch data
    cursor.execute(f"SELECT * FROM question_bank")
    rows = cursor.fetchall()

    # Convert rows to list of dictionaries
    data = []
    for row in rows:
        row_dict = dict(zip(columns, row))
        data.append(row_dict)

    connection.close()
    
    return jsonify(data)

# Route to authenticate user and generate JWT token
@app.route('/login', methods=["POST"])
@cross_origin()
def login():
    username = request.form["username"]
    password = request.form["password"]

    conn = sqlite3.connect('questionnaire.db')

    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    print('Opened database successfully')
    #print(request.form)

    cnt_users = conn.execute("SELECT count(*) FROM user_login where username = ? and password = ?", (username, password))

    temp_c = 0 
    for c in cnt_users:
        temp_c = c[0]

        
    if temp_c > 0:  # In a real scenario, password should be securely hashed
        token = jwt.encode({'user': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'username': username, 'token': token})

    # return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
    return make_response('Could not verify!', 401)



if __name__=='__main__':
    app.run(debug=True)
