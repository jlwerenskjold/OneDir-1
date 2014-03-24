from flask import Flask, url_for, render_template, request, g
import json
import os
import logging
import sqlite3
import hashlib
from werkzeug.utils import secure_filename

"""
The beginnings of a restful API for OneDir
"""

app = Flask(__name__)

UPLOAD_FOLDER = '/Users/Will/Desktop/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

try:
    CONNECTION = sqlite3.connect('users.db')
    CURSOR = CONNECTION.cursor()
except:
    exit()

@app.route('/users/create', methods=['POST'])
def create_user():
    if not request.json['username']:
        return "no username present"
    if not request.json['password']:
        return "no password present"
    username = request.json['username']
    password = request.json['password']
    hash = hashlib.sha256(password).hexdigest()
    try:
        CURSOR.execute("insert into Users (username, hash) values ('" + username + "','" + hash + "');")
        CONNECTION.commit()
    except:
        return "fail"
    return username

@app.route('/users/', methods=['GET'])
def show_users():
    CURSOR.execute("select * from Users")
    rows = CURSOR.fetchall()
    users = {}
    for row in rows:
        users[row[0]] = row[1]
    return render_template('users_template.html', users=users)

@app.route('/users/destroy/<user>')
def delete_user(user):
    try:
        CURSOR.execute("delete from Users where username='" + user + "';")
        CONNECTION.commit()
    except:
        return "failure"
    return user + " deleted"

@app.route('/users/<user>', methods=['GET'])
def get_user(user):
    CURSOR.execute("select * from Users where username='" + user + "'")
    rows = CURSOR.fetchall()
    users = {}
    for row in rows:
        users[row[0]] = row[1]
    return render_template("users_template.html", users=users)

@app.route('/authenticate', methods=['POST'])
def authenticate():
    if not request.json['username']:
        return "no username present"
    if not request.json['password']:
        return "no password present"
    username = request.json['username']
    password = request.json['password']
    CURSOR.execute("select * from Users where username='" + str(username) + "'")
    rows = CURSOR.fetchall()
    hash = hashlib.sha256(password).hexdigest()
    if rows[0][1] == hash:
        return "authenticated!"
    else:
        return "wrong password"



if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    # logging.basicConfig(filename='example.log',level=logging.DEBUG)
    logging.info("Starting server")
    app.run()
