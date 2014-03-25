from flask import Flask, url_for, render_template, request, redirect, flash, g
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, login_user , logout_user , current_user , login_required
import logging
import hashlib
from sqlalchemy import create_engine
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager
from werkzeug.utils import secure_filename
import os

#
#
# FLASK ONEDIR API
#
#

#
# GLOBAL VARIABLES
# Details the database, upload folders, and other configurations
#
app = Flask(__name__)
app.secret_key = 'super-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/Will/test.db'
UPLOAD_FOLDER = '/Users/Will/Desktop/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)

#
# USER MODEL
# SQLAlchemy model that interacts with SQLite database
#
class User(db.Model):
    __tablename__ = "users"
    id = db.Column('user_id',db.Integer , primary_key=True)
    username = db.Column('username', db.String(20), unique=True , index=True)
    password = db.Column('password' , db.String(10))
    email = db.Column('email',db.String(50),unique=True , index=True)

    def __init__(self , username ,password , email):
        self.username = username
        self.password = hashlib.sha256(password).hexdigest()
        self.email = email

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)

    def get_folder(self):
        folder = app.config['UPLOAD_FOLDER'] + "/" + str(self.username)
        if not os.path.exists(folder):
            os.makedirs(folder)
        return folder

# class File(db.Model):
#     __tablename__ = "file"
#     id = db.Column('user_id',db.Integer , primary_key=True)
#     username = db.Column('username', db.String(20), unique=True , index=True)
#     password = db.Column('password' , db.String(10))
#     email = db.Column('email',db.String(50),unique=True , index=True)
#
#     def __init__(self , username ,password , email):
#         self.username = username
#         self.password = hashlib.sha256(password).hexdigest()
#         self.email = email
# 
#     def is_authenticated(self):
#         return True
#
#     def is_active(self):
#         return True
#
#     def is_anonymous(self):
#         return False
#
#     def get_id(self):
#         return unicode(self.id)
#
#     def __repr__(self):
#         return '<User %r>' % (self.username)


#
# LOGIN MANAGER - in charge of sessions
#
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
    return User.query.filter_by(id=userid).first()

@login_manager.unauthorized_handler
def unauthorized():
    return '{ "result" : -1, "msg" : "unathorized"}'

@app.route('/file/<filename>', methods=['GET'])
@login_required
def get_file(filename):
    full_filename = os.path.join(current_user.get_folder(), filename)
    if not os.path.exists(full_filename):
        logging.warn("file does not exist on server: " + full_filename)
        return '{ "result" : -1, "msg" : "file does not exist"}'
    else:
        with open(full_filename, "rb") as in_file:
            read = in_file.read()
        return read

@app.route('/file', methods=['POST'])
@login_required
def upload_file():
    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_user.get_folder(), filename))
        file_url = str(url_for('get_file', filename=filename))
        return '{ "result" : 1, "msg" : "file uploaded"}'
    else:
        return '{ "result" : -1, "msg" : "file not uploaded"}'

@app.route('/register', methods=['POST'])
def register():
    if not request.json['username']:
        return "no username present"
    if not request.json['password']:
        return "no password present"
    if not request.json['email']:
        return "no password present"
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']
    hash = hashlib.sha256(password).hexdigest()
    try:
        user = User(username, password, email)
        db.session.add(user)
        db.session.commit()
    except:
        return '{ "result" : -1, "msg" : "validation failed"}'
    return '{ "result" :"' + str(username) + '", "msg" : "user created"}'

@app.route('/login', methods=['POST'])
def login():
    if not request.json['username']:
        return "no username present"
    if not request.json['password']:
        return "no password present"
    username = request.json['username']
    password = request.json['password']
    hash = hashlib.sha256(password).hexdigest()
    registered_user = User.query.filter_by(username=username,password=hash).first()
    if registered_user is None:
        return '{ "result" : -1, "msg" : "login faild"}'
    login_user(registered_user)
    return '{ "result" : "' + str(username) + '", "msg" : "authenticated"}'

@app.route('/logout', methods=['DELETE'])
def logout():
    if current_user:
            r = '{ "result" : "' + str(current_user.username) + '", "msg" : "logged out"}'
            logout_user()
    else:
        r = '{ "result" : -1, "msg" : "not logged in"}'
    return r

@app.errorhandler(404)
def not_found(error):
    return '{ "result" : -1, "msg" : "resource not found"}'

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run(threaded=True)