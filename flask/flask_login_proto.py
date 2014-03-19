from flask import Flask, url_for, render_template, request, redirect, flash, g
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, login_user , logout_user , current_user , login_required
import logging
import hashlib
from sqlalchemy import create_engine
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager

"""
Exploring flask-login library
"""

app = Flask(__name__)
app.secret_key = 'super-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/Will/test.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

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


login_manager = LoginManager()
login_manager.init_app(app)

engine = create_engine('sqlite:///:memory:', echo=True)

@app.before_request
def before_request():
    g.user = current_user

@login_manager.user_loader
def load_user(userid):
    return User.query.filter_by(id=userid).first()

@login_manager.unauthorized_handler
def unauthorized():
    return 'Unauthorized, please go <a href="' + str(url_for('login')) + '">here</a> to login'

@app.route('/register' , methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    user = User(request.form['username'] , request.form['password'],request.form['email'])
    db.session.add(user)
    db.session.commit()
    flash('User successfully registered')
    return redirect(url_for('login'))

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form['username']
    password = request.form['password']
    hash = hashlib.sha256(password).hexdigest()
    registered_user = User.query.filter_by(username=username,password=hash).first()
    if registered_user is None:
        flash('Username or Password is invalid' , 'error')
        return redirect(url_for('login'))
    login_user(registered_user)
    flash('Logged in successfully')
    return redirect(request.args.get('next') or url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/')
@login_required
def index():
    return render_template("index.html")

if __name__ == '__main__':
    # for database initialization, uncomment this
    # then run python flask_login_proto init, migrate, and upgrade cmds
    # manager.run()
    logging.basicConfig(level=logging.DEBUG)
    # logging.basicConfig(filename='example.log',level=logging.DEBUG)
    logging.info("Starting server")
    app.run()
