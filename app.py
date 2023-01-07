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
app.config['SECRET_KEY'] = secrets.token_hex(32)

Session(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods = ['POST'])
def post_login():
    pass

@app.route('/profile/<int:id>')
def profile(id):
    return render_template('profile.html')

@app.route('/profile/new')
def signup():
    return render_template('signup.html')

@app.route('/profile/new/elab', methods=['POST'])
def post_profile_new():
    pass

@app.route('/podcast/<int:id>')
def podcast(id):
    return render_template('podcast.html')

@app.route('/podcast/new', methods=['POST'])
def post_new_podcast():
    pass

@app.route('/episode/<int:id>')
def episode(id):
    return render_template('episode.html')

@app.route('/episode/new', methods=['POST'])
def post_new_episode():
    pass

@app.route('/comment/new', methods=['POST'])
def post_new_comment():
    pass

# Other routes

@app.route('/test')
def test():
    return render_template('test.html')

@app.errorhandler(404)
def page_not_found(error):
  # Create a response object
  return render_template('404.html')