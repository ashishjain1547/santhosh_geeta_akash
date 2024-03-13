from flask import Flask, redirect, render_template,request,url_for

from flask_bcrypt import Bcrypt

import json, requests

from flask_cors import CORS, cross_origin

from flask import Response, jsonify

import sqlite3

app=Flask(__name__)
bcrypt=Bcrypt(app)

@app.route('/')
def welcome():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    #print(request.form)
    username = ""
    password = ""
    retypepassword = ""
    
    if request.method=="POST":
        username=request.form["personname"]
        password=bcrypt.generate_password_hash(request.form["personpassword"]).decode('utf-8')
        retypepassword=request.form["personretypepassword"]
        print(username,password,retypepassword)
    # return render_template("result.html", username=username, password=password, retypepassword=retypepassword)

    

    conn = sqlite3.connect('sharks.db')

    # Creating a cursor object using the  
    # cursor() method 
    cursor = conn.cursor() 

    print('Opened database successfully')
    #print(request.form)

    # Creating table 
    table ="""CREATE TABLE IF NOT EXISTS USER_INFO (username VARCHAR(255), password VARCHAR(255))"""
    cursor.execute(table) 
    
    # Queries to INSERT records. 
    #query="INSERT INTO USER_INFO VALUES ('username",'password');"
    #cursor.execute(query)
    #query = "INSERT INTO USER_INFO VALUES (?, ?);"
    cursor.execute("INSERT INTO USER_INFO (username,password) VALUES (?, ?)", (username, password))
    #cursor.execute("INSERT INTO USER_INFO VALUES ('" + username + "', '" + password + "')") 
    conn.commit()
    conn.close()


    return "Data inserted sucessfully for: " + username
    # Redirect to the homepage if accessed via GET method
    
if __name__=='__main__':
    app.run(debug=True)
