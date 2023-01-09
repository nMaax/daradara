# Vanilla Python libraries
import os, re, secrets, sqlite3
from datetime import datetime, date, timedelta

# External files
import data.dao as dao
from login.models import User

# Flask libraries
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_session import Session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

SECRET_KEY = secrets.token_hex(32)
SESSION_TYPE = 'filesystem'
SESSION_PERMANENT = False

LOGIN_VIEW = 'post_login'
LOGIN_MSG = 'Accedi per visualizzare questa pagina'
LOGIN_MSG_CATEGORY = 'warning'

LOGIN_MAX_DURATION = timedelta(seconds=10)

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

app.config['SESSION_TYPE'] = SESSION_TYPE
app.config['SESSION_PERMANENT'] = SESSION_PERMANENT
Session(app)

login_manager = LoginManager()
#login_manager.login_view = LOGIN_VIEW # type: ignore
#login_manager.login_message = LOGIN_MSG
#login_manager.login_message_category = LOGIN_MSG_CATEGORY
login_manager.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login/elab', methods = ['POST'])
def post_login():
    # Get the username and password from the POST request
    email = request.form['email']
    password = request.form['password']

    # Retrieve the user from the database using the 'dao'
    user = dao.get_user_by_email(email)

    # Check if the user exists and the password is correct
    if user and True: #TODO check_password_hash(user.get('password'), password):
        # Login the user using Flask-Login's login_user function
        #TODO Imposta remeber in base alla checkbox remember me, metti duration a un valore più normale, non per il debug
        login_user(User(user), remember=True, duration=LOGIN_MAX_DURATION) 
        # Return a success message if the login works
        flash(message='Login effettuato', category='success')
        return redirect(url_for('index'))
    else:
        # Return an error message if the login fails
        flash('Invalid username or password', 'warning')
        return redirect(url_for('login'))

@app.route("/logout")
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
def post_signup():
    name = request.form['name']
    surname = request.form['surname']
    email = request.form['email']
    password = request.form['password']
    terms_agreement = request.form.get('terms')

    propic = 'propic.jpeg' #TODO gestire upload file
    #TODO rimuovi: creator = request.form['creator']

    # Check if all required fields are filled out
    if not name or not surname or not email or not password or not terms_agreement:
        flash("Unable to register, something went wrong", 'warning')
        return redirect(url_for('signup'))
    else:
        #TODO controlla che i dati inseriti siano corretti
        # Register user in database
        dao.new_user(email, password, name, surname, propic)
        flash("Successfully registered!", 'success')
        return redirect(url_for('index'))

@app.route('/podcast/<int:id>')
def podcast(id):
    podcast = dao.get_podcast(id)
    episodes = dao.get_episodes(id_podcast = id)
    tags = dao.get_tags(id)
    return render_template('podcast.html', id=id, podcast = podcast, episodes = episodes, tags = tags)

#TODO Trim and capitalize in order to don't have duplicates
@app.route('/podcast/new')
def new_podcast():
    return render_template('new-podcast.html')

#TODO Trim and capitalize in order to don't have duplicates
@app.route('/podcast/new/elab', methods=['POST'])
def post_new_podcast():
    title = request.form['title']
    desc = request.form['desc']
    img = 'podcast.jpeg'  #TODO gestire upload file
    tags = request.form['tags'] #TODO split the tags with ', '

    # Check if all required fields are filled out
    if not title or not desc or not img or not tags or not current_user:
        flash("Impossibile aggiugere il podcast, i dati iseriti sono mancanti o erronei", 'warning')
        return redirect(url_for('new_podcast'))
    else:
        #TODO controlla che i dati inseriti siano corretti
        # Register user in database
        user_id = current_user.id # type: ignore
        result = dao.new_podcast(title, desc, img, user_id, tags)
        if result:
            flash("Podcast aggiunto con successo!", 'success')
        else:
            flash("Impossibile aggiugere il podcast, qualcosa è andato storto, riprovare", 'warning')
        return redirect(url_for('profile', id = user_id))

@app.route('/podcast/<int:id>/delete/elab')
def post_delete_podcast(id):
    result = dao.delete_podcast(id)
    if result:
        flash(message='Podcast eliminato correttamente', category='success')
    else:
        flash(message='C\'è stato un errore durante l\'eliminazione del podcast, riporvare', category='success')
    return redirect(url_for('index'))

@app.route('/podcast/<int:id_pod>/episode/<int:id_ep>')
def episode(id_pod, id_ep):
    return render_template('episode.html')

#TODO Trim and capitalize in order to don't have duplicates
@app.route('/podcast/<int:id_pod>/episode/new')
def new_episode(id_pod):
    return render_template('new-episode.html', id_pod=id_pod)

#TODO Trim and capitalize in order to don't have duplicates
@app.route('/podcast/<int:id_pod>/episode/new/elab', methods=['POST'])
def post_new_episode(id_pod):
    title = request.form['title']
    desc = request.form['desc']
    audio = 'audio.mp4' #TODO imposta file
    timestamp = '2022-10-10' #TODO imposta timestamp = oggi
    id_podcast = id_pod
    # Check if all required fields are filled out
    if not title or not desc or not audio:
        flash("Impossibile aggiungere l'episodio, qualcosa è andato storto, riprovare", 'warning')
        return redirect(url_for('new_episode'))
    else:
        #TODO controlla che i dati inseriti siano corretti
        # Register episode in database
        dao.new_episode(title, desc, audio, timestamp, id_podcast)
        flash("Episodio aggiunto con successo!", 'success')
        return redirect(url_for('podcast', id = id_podcast))

@app.route('/podcast/<int:id_pod>/episode/delete/elab')
def post_delete_episode():
    pass

@app.route('/comment/new/elab', methods=['POST'])
def post_new_comment():
    pass

@app.route('/comment/delete/elab', methods=['POST'])
def post_delete_comment():
    pass

# Login manager - User Loader

@login_manager.user_loader
def load_user(user_id):
    return User(dao.get_user(user_id))

# Other routes

@app.route('/test')
def test():
    flash(message='Messaggio', category='dark')
    return render_template('test.html')

@app.route('/clear_session')
def clear_session():
    session.clear()
    return 'Session data cleared!'

@app.route('/clear_login')
def clear_login():
    logout_user()
    return 'Login data cleared!'

@app.errorhandler(404)
def page_not_found(error):
  return render_template('404.html', error=error)