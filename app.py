# Vanilla Python libraries
import os, re, sqlite3
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

@app.route('/')
def index():
    return render_template('layout.html')