from flask import Flask, url_for, render_template, request
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

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return url_for('get_file',
                                filename=filename)

@app.route('/upload', methods=['GET'])
def upload_form():
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/get_file/<filename>', methods=['GET'])
def get_file(filename):
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(full_filename):
        logging.warn("file does not exist on server: " + full_filename)
        return { "result" : -1, "msg" : "file does not exist"}
    else:
        with open(full_filename, "rb") as in_file:
            read = in_file.read(32)
        return read

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    # logging.basicConfig(filename='example.log',level=logging.DEBUG)
    logging.info("Starting server")
    app.run()
