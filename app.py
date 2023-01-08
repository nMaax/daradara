# Vanilla Python libraries
import os, re, secrets, sqlite3
from datetime import datetime, date

# External files
import data.dao as dao
from models import User

# Flask libraries
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_session import Session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.secret_key = '_5#y2L"F4Q8zcecowfm3]/'

Session(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # type: ignore

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login/elab', methods = ['POST'])
def post_login():
    # Get the username and password from the POST request
    username = request.form['username']
    password = request.form['password']

    # Retrieve the user from the database using the 'dao'
    user = dao.get_user_by_username(username)
    if not user:
        user = dao.get_user_by_email(username)

    # Check if the user exists and the password is correct
    if user and True: #TODO check_password_hash(user.get('password'), password):
        # Login the user using Flask-Login's login_user function
        login_user(User(user), True) #! Studia i vari parametri che login_user può avere
        # Return a success message if the login works
        flash(message='Login effettuato', category='success')
        return redirect(url_for('index'))
    else:
        # Return an error message if the login fails
        #flash('Invalid username or password', 'warning')
        return redirect(url_for('login'))

@app.route("/logout/elab")
@login_required
def logout():
    logout_user()
    #flash('Logout effettuato', 'info')
    return redirect(url_for('index'))

@app.route('/profile/<int:id>')
def profile(id):
    return render_template('profile.html')

#TODO Trim and capitalize in order to don't have duplicates
@app.route('/profile/new')
def signup():
    return render_template('signup.html')

@app.route('/profile/new/elab', methods=['POST'])
def post_profile_new():
    pass

@app.route('/podcast/<int:id>')
def podcast(id):
    return render_template('podcast.html')

#TODO Trim and capitalize in order to don't have duplicates
@app.route('/podcast/new', methods=['POST'])
def post_new_podcast():
    pass

@app.route('/episode/<int:id>')
def episode(id):
    return render_template('episode.html')

#TODO Trim and capitalize in order to don't have duplicates
@app.route('/episode/new', methods=['POST'])
def post_new_episode():
    pass

@app.route('/comment/new', methods=['POST'])
def post_new_comment():
    pass

# Login manager - User Loader

@login_manager.user_loader
def load_user(user_id):
    return User(dao.get_user(user_id))

# Other routes

@app.route('/test')
def test():
    return render_template('test.html')

@app.errorhandler(404)
def page_not_found(error):
  # Create a response object
  return render_template('404.html')