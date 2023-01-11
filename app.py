# Vanilla Python libraries
import os, re, secrets, sqlite3
from datetime import datetime, date, timedelta

# Personal libraries
import data.dao as dao
from data.errors.daoExceptions import dataManipulationError
from utils.models import User
from utils.detector import is_image, is_static_image, is_audio

# Flask libraries
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_session import Session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

# Constants

SECRET_KEY = secrets.token_hex(32)
SESSION_TYPE = 'filesystem'
SESSION_PERMANENT = False

#? Mi servono queste costanti?
LOGIN_VIEW = 'post_login'
LOGIN_MSG = 'Accedi per visualizzare questa pagina'
LOGIN_MSG_CATEGORY = 'warning'

LOGIN_MAX_DURATION = timedelta(seconds=60*60) # I login senza 'remember me' saranno cancellati dopo 60minuti

ISO_DATE = "%Y-%m-%d %H:%M:%S"

COVER_FOLDER = 'static/images/covers'

# App init

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

app.config['SESSION_TYPE'] = SESSION_TYPE
app.config['SESSION_PERMANENT'] = SESSION_PERMANENT
Session(app)

login_manager = LoginManager()
#? Cosa significano questi attributi?
#login_manager.login_view = LOGIN_VIEW # type: ignore
#login_manager.login_message = LOGIN_MSG
#login_manager.login_message_category = LOGIN_MSG_CATEGORY
login_manager.init_app(app)

# Routes

@app.route('/')
def index():
    if current_user.is_authenticated: # type: ignore
        saves = dao.get_saves_join_episodes_podcasts(current_user.id) # type: ignore
    else:
        saves = []
    onfire = dao.get_podcasts_onfire(number_of_podcasts=3)
    return render_template('index.html', saves=saves, onfire = onfire)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login/elab', methods = ['POST'])
def post_login():
    # Get the username and password from the POST request
    email = request.form['email']
    password = request.form['password']
    remember = request.form.get('remember')

    # Retrieve the user from the database using the 'dao'
    user = dao.get_user_by_email(email)

    # Check if the user exists and the password is correct
    if user and check_password_hash(user['password'], password): #TODO check_password_hash(user.get('password'), password):
        # Login the user using Flask-Login's login_user function
        #TODO Imposta remeber in base alla checkbox remember me, metti duration a un valore più normale, non per il debug
        if remember:
            login_user(User(user), remember=True, duration=LOGIN_MAX_DURATION)
        else:
            login_user(User(user), remember=False)
        # Return a success message if the login works
        flash(message='Login effettuato', category='success')
        return redirect(url_for('index'))
    else:
        # Return an error message if the login fails
        flash('Invalid username or password', 'warning')
        return redirect(url_for('login'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    #flash('Logout effettuato', 'info')
    return redirect(url_for('index'))

@app.route('/profile/<int:id>')
def profile(id):
    user = dao.get_user(id)
    podcasts = dao.get_podcasts_by_user(id_user=id)
    follows = dao.get_follows_join_podcasts(id_user=id)
    creators = dao.get_creators()
    is_creator = False
    if user and creators:
        for creator in creators:
            if creator['id'] == user['id']:
                is_creator = True
    else:
        flash(message='L\'utente cercato non esiste', category='warning')
        return redirect(url_for('index'))
    return render_template('profile.html', user=user, podcasts=podcasts, follows=follows, is_creator = is_creator)

#TODO Trim and capitalize in order to don't have duplicates
@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup/elab', methods=['POST'])
def post_signup():
    name = request.form['name']
    surname = request.form['surname']
    email = request.form['email']
    password = generate_password_hash(request.form['password'], method='sha256')
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
        login_user(User(dao.get_user_by_email(email)), remember=False)
        return redirect(url_for('index'))

@app.route('/podcast/<int:id>')
def podcast(id):
    podcast = dao.get_podcast(id)
    episodes = dao.get_episodes(id_podcast = id)
    category = dao.get_category(id)
    return render_template('podcast.html', id=id, podcast = podcast, episodes = episodes, category = category)

#TODO Trim and capitalize in order to don't have duplicates
@app.route('/podcast/new')
@login_required
def new_podcast():
    return render_template('new-podcast.html')

#TODO Trim and capitalize in order to don't have duplicates
@app.route('/podcast/new/elab', methods=['POST'])
@login_required
def post_new_podcast():

    # Retriving data 
    title = request.form['title']
    desc = request.form['desc']
    img = request.files['img']
    category = request.form['category']

    # Cleaning data
    title = title.strip()
    #title = title.capitalize()

    desc = desc.strip()
    #desc = desc.capitalize()

    category = category.strip()
    category = category.lower()
    
    #TODO! Check, via javascript, in the form that the max-min lengt is in the range ignoring whitespaces: ask to chatGPT how to do it
    check = True
    if not title or not desc or not img or not category:
        check = False
    elif len(title) < 4 or len(title) > 24:
        check = False
    elif dao.get_podcast_by_title(title) != []:
        check = False
    elif len(desc)<16 or len(desc) > 516:
        check = False
    elif len(category) < 4 or len(category) > 32:
        check = False
    elif not is_static_image(img.filename):
        check = False

    # Check if all required fields are filled out and if the user is logged in
    if not check:
        flash("Impossibile aggiugere il podcast, i dati iseriti sono mancanti o erronei", 'warning')
        return redirect(url_for('new_podcast'))
    elif not current_user.is_authenticated: # type: ignore
        flash("Fare il login prima di aggiungere il podcast", 'warning')
        return redirect(url_for('new_podcast'))
    else:
        
        # Retrive id of the creator and the id the podcast will have
        user_id = current_user.id # type: ignore
        podcast_id = dao.get_last_podcast_id() + 1

        # Define image name
        imgext = '.' + img.filename.split('.')[1] # type: ignore
        imgname = str(podcast_id) + imgext

        # If dao is unable to insert data, abort and do not save the image
        try:
            # Inserting entry in the database
            result = dao.new_podcast(title, desc, imgext, user_id, category)

            #TODO! con javascript controlla che non ci sia già un podcast con quel titolo
            if not result:
                raise dataManipulationError('Unable to add entry into the database')

            save_directory = 'static/uploads/images/covers/'
            if not os.path.exists(save_directory):
                os.makedirs(save_directory)
            img.save(save_directory+imgname) # type: ignore

            flash("Podcast aggiunto con successo!", 'success')
            return redirect(url_for('profile', id = user_id))
        except Exception as e:
            flash("Impossibile aggiugere il podcast, qualcosa è andato storto - ERR: " + str(e) + ", riprovare", 'danger')
            return redirect(url_for('new_podcast'))

@app.route('/podcast/<int:id>/delete/elab')
@login_required
def post_delete_podcast(id):
    result = dao.delete_podcast(id)
    if result:
        flash(message='Podcast eliminato correttamente', category='success')
    else:
        flash(message='C\'è stato un errore durante l\'eliminazione del podcast, riporvare', category='success')
    return redirect(url_for('index'))

#? Facciamo gli episodi con il loro numero dentro il podcast? O non ci conviene?
@app.route('/podcast/<int:id_pod>/episode/<int:id_ep>')
def episode(id_pod, id_ep):
    episode = dao.get_episode(id_ep)
    if episode and episode['id_podcast'] == id_pod:
        podcast = dao.get_podcast(id_pod)
        comments = dao.get_comments_extended(id_ep)
        return render_template('episode.html', id=id_ep, id_pod=id_pod, podcast=podcast, episode=episode, comments=comments)
    else:
        flash(message='Si è verificato un errore', category='danger')
        return redirect(url_for('index'))

@app.route('/podcast/<int:id_pod>/episode/new')
@login_required
def new_episode(id_pod):
    podcast = dao.get_podcast(id_pod)
    if not podcast:
        flash(message="Il podcast al quale hai cercato di aggiungere un episodio non esiste", category="warning")
        return redirect(url_for('index'))
    return render_template('new-episode.html', id_pod=id_pod, podcast=podcast)

#TODO Trim and capitalize in order to don't have duplicates
@app.route('/podcast/<int:id_pod>/episode/new/elab', methods=['POST'])
@login_required
def post_new_episode(id_pod):
    title = request.form['title']
    desc = request.form['desc']
    audio = 'audio.mp4' #TODO imposta file
    timestamp = datetime.now().strftime(ISO_DATE) #TODO imposta timestamp = oggi
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

@app.route('/podcast/<int:id_pod>/episode/<int:id_ep>/delete/elab')
def post_delete_episode(id_pod, id_ep):
    episode = dao.get_episode(id_ep)
    if episode and episode['id_podcast'] == id_pod:
        result = dao.delete_episode(id_ep)
        if result:
            flash(message='Episodio eliminato correttamente', category='success')
            return redirect(url_for('podcast', id=id_pod))
        else:
            flash(message='C\'è stato un errore durante l\'eliminazione dell\'episodio, riporvare', category='danger')
            return redirect(url_for('index'))
    else:
        flash(message='Si è verificato un errore', category='danger')
        return redirect(url_for('index'))

@app.route('/podcast/<int:id_pod>/episode/<int:id_ep>/comment/new/elab', methods=['POST'])
@login_required
def post_new_comment(id_pod, id_ep):
    episode = dao.get_episode(id_ep)
    if episode and episode['id_podcast'] == id_pod:
        text = request.form['text']
        timestamp = datetime.now().strftime(ISO_DATE)
        result = dao.new_comment(id_user=current_user.id, id_ep=id_ep, text=text, timestamp=timestamp)  # type: ignore
        if not result:
            flash(message='C\'è stato un errore durante l\'aggiunta del commento, riporvare', category='danger')
        return redirect(url_for('episode', id_ep=id_ep, id_pod=id_pod))
    else:
        flash(message='Si è verificato un errore', category='danger')
        return redirect(url_for('index'))

@app.route('/podcast/<int:id_pod>/episode/<int:id_ep>/comment/delete/elab', methods=['POST'])
@login_required
def post_delete_comment(id_pod, id_ep):
    episode = dao.get_episode(id_ep)
    if episode and episode['id_podcast'] == id_pod:
        timestamp = request.form['timestamp']
        #TODO rename delete_comment_by_PK in something else
        #! Se provi a cancellare il commento di un altro flash dice che ci sei riuscito ma in realtà non è andato via
        result = dao.delete_comment_by_PK(id_ep=id_ep, id_user=current_user.id, timestamp=timestamp) # type: ignore
        if result:
            flash(message='Commento eliminato correttamente', category='success')
            return redirect(url_for('episode', id_ep=id_ep, id_pod=id_pod))
        else:
            flash(message='C\'è stato un errore durante l\'eliminazione del commento, riporvare', category='danger')
            return redirect(url_for('episode', id_ep=id_ep, id_pod=id_pod))
    else:
        flash(message='Si è verificato un errore', category='danger')
        return redirect(url_for('index'))

# Login manager

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

# Functions