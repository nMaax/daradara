# Vanilla Python libraries
import os, re, secrets
from random import randint
from datetime import datetime, timedelta
from dateutil import parser as date_parser

# Personal libraries
import data.dao as dao
from data.errors.daoExceptions import dataManipulationError, notPodcastOwnerError
from utils.models import User
from utils.detector import is_static_image, is_audio
from utils.cropper import make_square
from utils.utils import days_ago, add_days_ago, to_list_of_dict

# Flask libraries
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_session import Session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

# Flask-Session constants
SECRET_KEY = secrets.token_hex(32)
SESSION_TYPE = 'filesystem'
SESSION_PERMANENT = False

# Flask-Login constants
LOGIN_MAX_DURATION = timedelta(seconds=60*60) # I login senza 'remember me' saranno cancellati dopo 60 minuti

# Date constants
ISO_DATE = "%Y-%m-%d"
ISO_TIME = "%H:%M:%S"
ISO_TIMESTAMP = ISO_DATE + " " + ISO_TIME
DEFAULT_HOUR = "00:00:00"

# Saving path constants
PROPICS_PATH = 'static/uploads/images/propics/'
COVERS_PATH = 'static/uploads/images/covers/'
AUDIOS_PATH = 'static/uploads/audios/'

# App init
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

# Session init
app.config['SESSION_TYPE'] = SESSION_TYPE
app.config['SESSION_PERMANENT'] = SESSION_PERMANENT
Session(app)

# Login init
login_manager = LoginManager()
login_manager.init_app(app)

# Routes
@app.route('/')
def index():
    saves= []
    if current_user.is_authenticated: # type: ignore
        saves = dao.get_saves_join_episodes_podcasts(current_user.id) # type: ignore
    onfire = add_days_ago(dao.get_podcasts_onfire(number_of_podcasts=3))
    session['previous_url'] = request.url
    return render_template('index.html', saves=saves, onfire=onfire)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login/elab', methods = ['POST'])
def post_login():
    # Get the username and password from the POST request
    email = request.form['email']
    password = request.form['password']
    remember = request.form.get('remember')

    # Retrieve the user from the database using dao
    user = dao.get_user_by_email(email)

    # Check if the user exists and the password is correct
    if user and check_password_hash(user['password'], password):
        # Login the user using Flask-Login's login_user function
        if remember:
            login_user(User(user), remember=True, duration=LOGIN_MAX_DURATION)
        else:
            login_user(User(user), remember=False, duration=LOGIN_MAX_DURATION)
        # Return a success message if the login works
        flash(message='Login effettuato con successo!', category='success')
        return redirect(session.get('previous_url', '/'))
    else:
        # Return an error message if the login fails
        flash('Email e password non corretti, riprovare', 'warning')
        return redirect(url_for('login'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout effettuato', 'success')
    return redirect(session.get('previous_url', '/'))

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup/elab', methods=['POST'])
def post_signup():

    # Retrive data from the form
    name = request.form['name']
    surname = request.form['surname']
    email = request.form['email']
    password = request.form['password']
    propic = request.files['propic']
    terms_agreement = request.form.get('terms')
    
    # Clean the data 
    name = name.strip()
    name = name.title()
    surname = surname.strip()
    surname = surname.title()
    email = email.strip()

    # Check if all form fields are filled out and that each value is not violating the rules
    check = True
    if not name or not surname or not email or not password or not terms_agreement or not propic:
        check = False
    elif len(name) < 2 or len(name) > 32:
        check = False
    elif len(surname) < 2 or len(surname) > 32:
        check = False
    elif len(email) < 6 or not email.__contains__('@') or not email.__contains__('.'):
        check = False
    elif len(password) < 8 or not re.search("[A-Z]", password) or not re.search("[a-z]", password) or not re.search("[0-9]", password):
        check = False
    elif not is_static_image(secure_filename(propic.filename)): # type: ignore
        check = False

    # If the data isn't correct say it, otherwhise continue 
    if not check:
        flash("Dati inseriti mancanti o erronei, riprovare", 'warning')
        return redirect(url_for('signup'))
    elif dao.get_user_by_email(email):
        flash("Esiste già un utente con quella email", 'warning')
        return redirect(url_for('signup'))
    else:
        # Get what will the new user id be
        user_id = dao.get_last_id_user() + 1

        # Define image name
        filename = secure_filename(propic.filename) # type: ignore
        propicext = '.' + filename.split('.')[-1] # type: ignore
        propicname = str(user_id) + propicext

        try:
            # Register user in database
            password = generate_password_hash(request.form['password'], method='sha256')
            result = dao.new_user(email, password, name, surname, propicext)

            if not result:
                raise dataManipulationError('Unable to register new user')

            # Save the propic (only if the user has been saved)
            save_directory = PROPICS_PATH
            if not os.path.exists(save_directory):
                os.makedirs(save_directory)
            propic = make_square(propic)
            propic.save(save_directory+propicname) # type: ignore
            
            
            # Automatic login after registration
            login_user(User(dao.get_user_by_email(email)), remember=False)
            
            flash("Utente registrato correttamente!", 'success')
            return redirect(session.get('previous_url')) #redirect(url_for('profile', id=user_id)) # type: ignore
        except Exception as e:
            flash("Impossibile registrare il nuovo utente, qualcosa è andato storto - ERR: " + str(e), 'danger')
            return redirect(url_for('signup'))

@app.route('/profile/<int:id>')
def profile(id: int):
    user = dao.get_user(id)
    

    if not user:
        flash(message='L\'utente cercato non esiste', category='warning')
        return redirect(session.get('previous_url', '/'))

    podcasts = dao.get_podcasts_by_user(id_user=id)
    follows = dao.get_follows_join_podcasts(id_user=id)
    saves = dao.get_saves_join_episodes_podcasts(id_user=id)
    privacy = [dao.get_priv_owned(id), dao.get_priv_follows(id), dao.get_priv_saves(id)]

    creators = dao.get_creators()
    is_creator = False
    if creators:
        for creator in creators:
            if creator['id'] == user['id']:
                is_creator = True

    is_owner = False
    if current_user.is_authenticated and current_user.id == id: # type: ignore
        is_owner = True

    session['previous_url'] = request.url
    return render_template('profile.html', user=user, podcasts=podcasts, follows=follows, saves=saves, privacy=privacy, is_creator=is_creator, is_owner=is_owner)
        
    
@app.route('/profile/<int:id>/podcasts')
def owned(id: int):
    user = dao.get_user(id)

    if not user:
        flash('L\'utente cercato non esiste', 'warning')
        return redirect(session.get('previous_url', '/'))

    podcasts = dao.get_podcasts_by_user(id)

    is_owner = False
    if current_user.is_authenticated and current_user.id == id: # type: ignore
        is_owner = True

    if not is_owner and user['priv_owned'] == 1:
        flash('A gli altri utenti non è permesso vedere i podcast di questo profilo', 'info')
        return redirect(url_for('profile', id=id))

    session['previous_url'] = request.url
    return render_template('owned.html', user=user, podcasts=podcasts, is_owner=is_owner)
        

@app.route('/profile/<int:id>/priv_owned')
@login_required
def privatize_owned(id: int):
    user = dao.get_user(id)
    if user and current_user.id == id: # type: ignore 
        dao.switch_priv_owned(id)
        return redirect(url_for('profile', id=id)+"#owned")
    else:
        flash('Non puoi modificare le impostazioni di un altro account', 'warning')
        return redirect(session.get('previous_url', '/'))

@app.route('/profile/<int:id>/follows')
def follows(id: int):
    user = dao.get_user(id)

    if not user:
        flash('L\'utente cercato non esiste', 'warning')
        return redirect(session.get('previous_url', '/'))

    podcasts = dao.get_follows_join_podcasts(id)

    is_owner = False
    if current_user.is_authenticated and current_user.id == id: # type: ignore
        is_owner = True

    if not is_owner and user['priv_follows'] == 1:
        flash('A gli altri utenti non è permesso vedere i seguiti di questo profilo', 'info')
        return redirect(url_for('profile', id=id))

    session['previous_url'] = request.url
    return render_template('follows.html', user=user, podcasts=podcasts, is_owner=is_owner)
        

@app.route('/profile/<int:id>/priv_follows')
@login_required
def privatize_follows(id: int):
    user = dao.get_user(id)
    if user and current_user.id == id: # type: ignore 
        dao.switch_priv_follows(id)
        return redirect(url_for('profile', id=id))
    else:
        flash('Non puoi modificare le impostazioni di un altro account', 'warning')
        return redirect(session.get('previous_url', '/'))

@app.route('/profile/<int:id>/saves')
def saves(id: int):
    user = dao.get_user(id)

    if not user:
        flash('L\'utente cercato non esiste', 'warning')
        return redirect(session.get('previous_url', '/'))

    episodes = dao.get_saves_join_episodes_podcasts(id)

    is_owner = False
    if current_user.is_authenticated and current_user.id == id: # type: ignore
        is_owner = True

    if not is_owner and user['priv_saves'] == 1:
        flash('A gli altri utenti non è permesso vedere gli episodi salvati di questo profilo', 'info')
        return redirect(url_for('profile', id=id))

    session['previous_url'] = request.url
    return render_template('saves.html', user=user, episodes=episodes, is_owner=is_owner)
        

@app.route('/profile/<int:id>/priv_saves')
@login_required
def privatize_saves(id: int):
    user = dao.get_user(id)
    if user and current_user.id == id: # type: ignore 
        dao.switch_priv_saves(id)
        return redirect(url_for('profile', id=id)+"#saves")
    else:
        flash('Non puoi modificare i le impostazioni di un altro account', 'warning')
        return redirect(session.get('previous_url', '/'))

@app.route('/profile/<int:id>/bio/edit/elab', methods=['POST'])
@login_required
def post_edit_bio(id: int):

    # Retriving data 
    bio = request.form['bio']

    # Cleaning data
    bio.strip()
    
    # Checking data
    check = True
    if len(bio) > 516:
        check = False
    elif bio == None or bio == "":
        bio = None

    # If the profile doesnt exist or the user that is trying to edit it is not the owner abort (and say it)
    user = dao.get_user(id)
    if not user:
        flash(message='Il profilo dove hai richiesto la modifica della bio non esiste', category='warning')
        return redirect(session.get('previous_url', '/'))
    elif user['id'] != current_user.id: # type: ignore
        flash(message='Non sei il proprietario del profilo', category='warning')
        return redirect(url_for('profile', id=id))
    elif not check:
        flash(message='I dati sono mancanti o erronei, riprovare', category='warning')
        return redirect(url_for('profile', id=id))
    else:
        # Otherwise save the data
        try:

            if user['bio'] == bio:
                bio = None

            result = dao.update_user_bio(id, bio)

            if not result:
                raise dataManipulationError('Unable to update bio')

            flash(message='Biografia modificata correttamente', category='success')
        
        # If something bad happens, abort and say it
        except Exception as e:
            flash(message='C\'è stato un errore durante la modifica della biografia - ERR: '+str(e), category='danger')
        
        return redirect(url_for('profile', id=id))

@app.route('/profile/<int:id>/propic/edit/elab', methods=['POST'])
def post_update_propic(id):

    # Retriving data 
    img = request.files['img']

    # Checking data
    check = True
    if not img or not is_static_image(secure_filename(img.filename)): # type: ignore
        check = False

    # If the profile doesnt exist or the user that is trying to edit it is not the owner abort (and say it)
    user = dao.get_user(id)

    if not user:
        flash('Il profilo dove hai richiesto la modifica dell\'immagine non esiste', 'warning')
    elif user['id'] != current_user.id: # type: ignore
        flash('Non sei il propriterio del profilo', 'warning')
    elif not check:
        flash("Impossibile modificare l'immagine, il file fornito non è compatibile", 'warning')
    else:
        # Otherwise save the data
        try:

            # Define filename and file extension
            filename = secure_filename(img.filename) # type: ignore
            imgext = '.' + filename.split('.')[-1] # type: ignore
            imgname = str(id) + imgext

            # Save the image
            save_directory = PROPICS_PATH
            if not os.path.exists(save_directory):
                os.makedirs(save_directory)
            img = make_square(img)
            img.save(save_directory+imgname) # type: ignore

            # Delete old image if it has a different extension
            if user['propic'] != imgext:
                old_imgext = user['propic']
                old_imgname = str(id) + old_imgext
                old_file_path = save_directory + old_imgname
                if os.path.exists(old_file_path):
                    os.remove(old_file_path)

            # Update the image extension in the db
            result = dao.update_user_img(id, img=imgext)

            if not result:
                raise dataManipulationError('Unable to update the image')

            flash('Immagine modificata correttamente', 'success')

        # If something bad happens, abort and say it
        except Exception as e:
            flash("Impossibile aggiornare l'immagine, qualcosa è andato storto - ERR: " + str(e), 'danger')

    return redirect(url_for('profile', id=id))

@app.route('/podcast/<int:id>')
def podcast(id: int):
    podcast = dao.get_podcast(id)
    
    if not podcast:
        flash(message='Il podcast cercato non esiste', category='warning')
        return redirect(session.get('previous_url', '/'))

    creator = dao.get_user(podcast['id_user'])

    row_last_update = dao.get_last_update(id)
    last_update = row_last_update['last_update'] # type: ignore
    if last_update:
        last_update = days_ago(last_update)
    else:
        last_update = False

    episodes = to_list_of_dict(dao.get_episodes(id_podcast=id))
    for episode in episodes:
        mime_type = 'mpeg'
        if episode['audio'] == '.wav':
            mime_type='wav'
        episode['mime_type'] = mime_type 
    
    is_owner = False
    is_following = False
    if current_user.is_authenticated: # type: ignore
        is_following = dao.is_following(id_user=current_user.id, id_pod=id) # type: ignore
        is_owner = podcast['id_user'] == current_user.id # type: ignore

    session['last_podcast_visited'] = id
    session['previous_url'] = request.url
    return render_template('podcast.html', id=id, podcast=podcast, episodes=episodes, last_update=last_update, creator=creator, is_following=is_following, is_owner=is_owner)

@app.route('/podcast/<int:id>/follow')
def follow(id: int):

    if not current_user.is_authenticated: # type: ignore
        flash('Fai l\'accesso per seguire il podcast', 'info')
        return redirect(url_for('podcast', id=id))

    podcast = dao.get_podcast(id)
    if podcast:
        dao.follow(id_pod=id, id_user=current_user.id, timestamp=datetime.now().strftime(ISO_TIMESTAMP)) # type: ignore 
        return redirect(url_for('podcast', id=id))
    else:
        flash('Non puoi seguire un podcast che non esiste', 'warning')
        return redirect(session.get('previous_url', '/'))

@app.route('/podcast/<int:id>/unfollow')
@login_required
def unfollow(id: int):
    podcast = dao.get_podcast(id)
    if podcast:
        dao.unfollow(id_pod=id, id_user=current_user.id) # type: ignore 
        return redirect(url_for('podcast', id=id))
    else:
        flash('Non puoi smettere di seguire un podcast che non esiste', 'warning')
        return redirect(session.get('previous_url', '/'))

@app.route('/podcast/new')
def new_podcast():
    if not current_user.is_authenticated: # type: ignore
        flash('Fai l\'accesso per poter creare un podcast', category='info')

    return render_template('newpodcast.html')

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
    desc = desc.strip()
    category = category.strip()
    category = category.lower()
    
    # Checking data
    check = True
    if not title or not desc or not img or not category:
        check = False
    elif len(title) < 4 or len(title) > 32:
        check = False
    elif len(desc)<16 or len(desc) > 516:
        check = False
    elif len(category) < 4 or len(category) > 32:
        check = False
    elif not is_static_image(secure_filename(img.filename)): # type: ignore
        check = False

    # Check if all form fields are filled out and that each value is not violating the rules
    if not check:
        flash("Impossibile aggiugere il podcast, i dati iseriti sono mancanti o erronei", 'warning')
        return redirect(url_for('new_podcast'))
    elif dao.get_podcast_by_title(title):
        flash("Esiste già un podcast con questo titolo", 'warning')
        return redirect(url_for('new_podcast'))
    else:

        # Retrive the id of the creator and the id the podcast will have
        user_id = current_user.id # type: ignore
        podcast_id = dao.get_last_podcast_id() + 1

        # If dao is unable to insert data, abort and do not save the image
        try:
            # Define image name
            filename = secure_filename(img.filename) # type: ignore
            imgext = '.' + filename.split('.')[-1] # type: ignore
            imgname = str(podcast_id) + imgext

            # Inserting entry in the database
            result = dao.new_podcast(title, desc, imgext, user_id, category)

            if not result:
                raise dataManipulationError('Unable to add entry into the database')

            # Save the image (only if the podcast has been saved)
            save_directory = COVERS_PATH
            if not os.path.exists(save_directory):
                os.makedirs(save_directory)
            img.save(save_directory+imgname) # type: ignore

            flash("Podcast aggiunto con successo!", 'success')
            return redirect(url_for('profile', id = user_id))
        except Exception as e:
            flash("Impossibile aggiugere il podcast, qualcosa è andato storto - ERR: " + str(e), 'danger')
            return redirect(url_for('new_podcast'))

@app.route('/podcast/<int:id>/delete/elab')
@login_required
def post_delete_podcast(id: int):

    podcast = dao.get_podcast(id)
    episodes = dao.get_episodes(id)

    # If the podcast doesnt exist or the user that is trying to delete it is not the owner abort
    if not podcast:
        flash(message='Il podcast che hai richiesto di eliminare non esiste', category='warning')
        return redirect(session.get('previous_url', '/'))
    elif podcast['id_user'] != current_user.id: # type: ignore
        flash(message='Non sei il proprietario del podcast', category='warning')
        return redirect(url_for('podcast', id=id))

    # Otherwise delete the podcast (and its episodes)
    result = dao.delete_podcast(id)

    if not result:
        flash(message='C\'è stato un errore durante l\'eliminazione del podcast, riprovare', category='danger')
        return redirect(url_for('podcast', id=podcast['id']))

    # Delete the podcast image
    file_path = COVERS_PATH+str(podcast['id'])+podcast['img']
    abs_path = os.path.abspath(file_path)
    if os.path.exists(abs_path):
            os.remove(abs_path)

    # Delete the aduio of the episodes (the entries are already deleted with dao)
    for episode in episodes:
        file_path = AUDIOS_PATH+str(episode['id'])+episode['audio']
        abs_path = os.path.abspath(file_path)
        if os.path.exists(abs_path):
            os.remove(abs_path)

    flash(message='Podcast eliminato correttamente', category='success')
    return redirect(url_for('index'))

@app.route('/podcast/<int:id>/edit/elab', methods=['POST'])
@login_required
def post_edit_podcast(id: int):

    # Retriving data 
    title = request.form['title']
    desc = request.form['desc']
    category = request.form['category']

    # Cleaning data
    title = title.strip()
    desc = desc.strip()
    category = category.strip()
    category = category.lower()
    
    # Checking the data
    check = True
    if not title or not desc or not category:
        check = False
    elif len(title) < 4 or len(title) > 32:
        check = False
    elif len(desc)<16 or len(desc) > 516:
        check = False
    elif len(category) < 4 or len(category) > 32:
        check = False

    # If the podcast doesnt exist or the user that is trying to edit it is not the owner or the data inserted is not correct abort
    podcast = dao.get_podcast(id)
    if not podcast:
        flash(message='Il podcast di cui hai richiesto l\'eliminazione non esiste', category='warning')
        return redirect(session.get('previous_url', '/'))
    elif podcast['id_user'] != current_user.id: # type: ignore
        flash(message='Non sei il proprietario del podcast', category='warning')
        return redirect(url_for('podcast', id=id))
    elif not check:
        flash(message='I dati sono mancanti o erronei, riprovare', category='warning')
        return redirect(url_for('podcast', id=id))
    else:
        try:

            if podcast['title'] == title:
                title = None
            if podcast['desc'] == desc:
                desc = None
            if podcast['tag'] == category:
                category = None

            if dao.get_podcast_by_title(title):
                raise dataManipulationError('A podcast with that title already exists')

            # Otherwise edit the podcast
            if title or desc:
                pod_result = dao.update_podcast(id=id, title=title, desc=desc)
            else:
                pod_result = True

            if category:
                tag_result = dao.update_category(id_pod=id, category=category)
            else:
                tag_result = True

            if not pod_result:
                raise dataManipulationError('Unable to update title or description')
            elif not tag_result:
                raise dataManipulationError('Unable to update category')

            flash(message='Podcast modificato correttamente', category='success')
                
        except Exception as e:
            flash(message='C\'è stato un errore durante la modifica del podcast - ERR: '+str(e), category='danger')
        
        return redirect(url_for('podcast', id=id))

@app.route('/podcast/<int:id>/cover/edit/elab', methods=['POST'])
def post_update_podcast_img(id: int):
    
    # Retriving data
    img = request.files['img']

    # Checking data
    check = True
    if not img:
        check = False
    elif not is_static_image(secure_filename(img.filename)): # type: ignore
        check = False

    podcast = dao.get_podcast(id)
    if not check:
        flash("Impossibile modificare l'immagine, il file fornito non è compatibile", 'warning')
    elif not podcast:
        flash("Impossibile modificare l'immagine, il podcast non esiste", 'warning')
    elif podcast['id_user'] != current_user.id: # type: ignore
        flash("Impossibile modificare l'immagine, non sei il proprietario del podcast", 'warning')
    else:
        try:

            # Define image name and extension
            filename = secure_filename(img.filename) # type: ignore
            imgext = '.' + filename.split('.')[-1] # type: ignore
            imgname = str(id) + imgext

            # Save the image (only if the podcast has been saved)
            save_directory = COVERS_PATH
            if not os.path.exists(save_directory):
                os.makedirs(save_directory)
            img = make_square(img)
            img.save(save_directory+imgname) # type: ignore

            # Delete old image if it has a different extension
            if podcast['img'] != imgext:
                old_imgext = podcast['img']
                old_imgname = str(id) + old_imgext
                old_file_path = save_directory + old_imgname
                if os.path.exists(old_file_path):
                    os.remove(old_file_path)

            result = dao.update_podcast(id, img=imgext)

            if not result:
                raise dataManipulationError('Unable to update the image')

            flash('Immagine modificata correttamente', 'success')

        except Exception as e:
            flash("Impossibile aggiornare l'immagine, qualcosa è andato storto - ERR: " + str(e), 'danger')

    return redirect(url_for('podcast', id=id))

@app.route('/podcast/<int:id_pod>/episode/<int:id_ep>')
def episode(id_pod: int, id_ep: int):
    episode = dao.get_episode(id_ep)
    if episode and episode['id_podcast'] == id_pod:
        daysago = days_ago(episode['timestamp'])
        podcast = dao.get_podcast(id_pod)
        comments = dao.get_comments_join_users(id_ep)
        if comments:
            comments = add_days_ago(comments)

        mime_type = 'mpeg'
        if episode['audio'] == '.wav':
            mime_type='wav'

        is_owner = False
        has_saved = False
        if current_user.is_authenticated: # type: ignore
           has_saved = dao.has_saved(id_user=current_user.id, id_ep=id_ep) # type: ignore
           is_owner = podcast['id_user'] == current_user.id # type: ignore
        
        session['last_podcast_visited'] = id_pod
        session['previous_url'] = request.url
        return render_template('episode.html', id=id_ep, id_pod=id_pod, podcast=podcast, episode=episode, daysago=daysago, comments=comments, mime_type=mime_type, has_saved=has_saved, is_owner=is_owner)
    else:
        flash(message='L\'episodio che hai provato di aprire non appartiene a questo podcast', category='warning')
        return redirect(session.get('previous_url', '/'))

@app.route('/podcast/<int:id_pod>/episode/<int:id_ep>/save')
def save(id_pod :int, id_ep: int):

    if not current_user.is_authenticated: # type: ignore
        flash('Fai l\'accesso per salvare l\'episodio', 'info')
        return redirect(url_for('episode', id_ep=id_ep, id_pod=id_pod))

    episode = dao.get_episode(id_ep)
    if episode and episode['id_podcast'] == id_pod:
        dao.save(id_ep=id_ep, id_user=current_user.id, timestamp=datetime.now().strftime(ISO_TIMESTAMP)) # type: ignore 
        return redirect(url_for('episode', id_ep=id_ep, id_pod=id_pod))
    else:
        flash('Non puoi seguire un episodio che non esiste', 'warning')
        return redirect(session.get('previous_url', '/'))

@app.route('/podcast/<int:id_pod>/episode/<int:id_ep>/unsave')
@login_required
def unsave(id_pod :int, id_ep: int):
    episode = dao.get_episode(id_ep)
    if episode and episode['id_podcast'] == id_pod:
        dao.unsave(id_ep=id_ep, id_user=current_user.id) # type: ignore 
        return redirect(url_for('episode', id_ep=id_ep, id_pod=id_pod))
    else:
        flash('Non puoi smettere di seguire un episodio che non esiste', 'warning')
        return redirect(session.get('previous_url', '/'))

@app.route('/podcast/<int:id_pod>/episode/new')
@login_required
def new_episode(id_pod: int):
    podcast = dao.get_podcast(id_pod)
    if not podcast:
        flash('Il podcast nel quale hai cercato di creare l\'episodio non esiste', 'warning')
        return redirect(session.get('previous_url', '/'))
    elif podcast['id_user'] != current_user.id: # type: ignore
        flash('Non sei il proprietario del podcast', 'warning')
        return redirect(url_for('podcast', id=id_pod))
    else:
        return render_template('newepisode.html', id_pod=id_pod, podcast=podcast)

@app.route('/podcast/<int:id_pod>/episode/new/elab', methods=['POST'])
@login_required
def post_new_episode(id_pod: int):
    
    # Retriving data
    title = request.form['title']
    desc = request.form['desc']
    audio = request.files['audio']
    date = request.form['date']

    # Cleaning data
    title = title.strip()
    desc = desc.strip()
    
    #TODO! Check, via javascript, in the form that the max-min lengt is in the range ignoring whitespaces: ask to chatGPT how to do it
    # Checking that the data is valid
    check = True
    if not title or not desc or not audio:
        check = False
    elif len(title) < 4 or len(title) > 32:
        check = False
    elif len(desc) < 16 or len(desc) > 516:
        check = False
    elif not is_audio(secure_filename(audio.filename)): # type: ignore
        check = False

    # Checking the date input, if for any reason the user sended something that python can't recognize as a date it will default to the now timestamp
    try:
        py_date = date_parser.parse(date) # date_parser(date) takes a string and converts it to a datetime object (if the parameter is not recognized as a date raises an Error that the try except will catch)
        min_date = datetime(2022, 1, 1)
        max_date = datetime.now()

        if py_date.date() < min_date.date():
            raise ValueError("The date is before the date lower bound")
        elif py_date.date() > max_date.date():
            raise ValueError("The date is after the date upper bound (today)")
        elif py_date.date() == datetime.now().date():
            timestamp = datetime.now().strftime(ISO_TIMESTAMP)
        else:
            timestamp = py_date.strftime(ISO_DATE) + " " + DEFAULT_HOUR

    except Exception as e:
        flash("E' stata inserita una data in un formato non corretto, conseguentemente questa è stata cambiata all'istante odierno - ERR: "+str(e), 'info')
        timestamp = datetime.now().strftime(ISO_TIMESTAMP)

    # Check if all required fields are filled out and if the user is logged in
    if not check:
        flash("Impossibile aggiugere l'episodio, i dati iseriti sono mancanti o erronei", 'warning')
        return redirect(url_for('new_episode', id_pod=id_pod))
    else:

         # Retrive id of the creator and the id the episode will have
        user_id = current_user.id # type: ignore
        episode_id = dao.get_last_episode_id() + 1

        # Define audio name
        filename = secure_filename(audio.filename) # type: ignore
        audioext = '.' + filename.split('.')[-1]
        audioname = str(episode_id) + audioext

        # If dao is unable to insert data, abort and do not save the audio
        try:

            if not dao.get_podcast(id_pod)['id_user'] == user_id: # type: ignore
                raise notPodcastOwnerError('You are not the owner of the podcast')

            # Inserting entry in the database
            result = dao.new_episode(title, desc, audioext, timestamp, id_podcast=id_pod)
            if not result:
                raise dataManipulationError('Unable to add entry into the database')

            # Save the audio
            save_directory = AUDIOS_PATH
            if not os.path.exists(save_directory):
                os.makedirs(save_directory)
            audio.save(save_directory+audioname) # type: ignore

            flash("Episodio aggiunto con successo!", 'success')
            return redirect(url_for('podcast', id = id_pod))
        except Exception as e:
            flash("Impossibile aggiugere l'episodio, qualcosa è andato storto - ERR: " + str(e), 'danger')
            return redirect(url_for('new_episode', id_pod=id_pod))

@app.route('/podcast/<int:id_pod>/episode/<int:id_ep>/delete/elab')
@login_required
def post_delete_episode(id_pod: int, id_ep: int):
    episode = dao.get_episode(id_ep)
    podcast = dao.get_podcast(id_pod)

    if not episode or not podcast:
        flash('L\'episodio che hai richiesto di eliminare non esiste', category='warning')
        return redirect(session.get('previous_url', '/'))
    elif episode['id_podcast'] != id_pod:
        flash('L\'episodio e il podcast nell\'url non corrispondono', category='warning')
        return redirect(session.get('previous_url', '/'))
    elif podcast['id_user'] != current_user.id: # type: ignore
        flash('Non sei il proprietario del podcast', category='warning')
        return redirect(url_for('episode', id_pod=id_pod, id_ep=id_ep))
    else:
        result = dao.delete_episode(id_ep)
        if result:
            #TODO! in cascata devi eliminare anche tutti gli audio
            #path = os.path.join(app.root_path, url_for('static', filename='uploads/audios/'+str(episode['id'])+episode['img']))
            file_path = AUDIOS_PATH+str(episode['id'])+episode['audio']
            abs_path = os.path.abspath(file_path)
            if os.path.exists(abs_path):
                os.remove(abs_path)

            flash(message='Episodio eliminato correttamente', category='success')
            return redirect(url_for('podcast', id=id_pod))
        else:
            flash(message='C\'è stato un errore durante l\'eliminazione dell\'episodio, riporvare', category='danger')
            return redirect(url_for('episode', id_pod=id_pod, id_ep=id_ep))

@app.route('/podcast/<int:id_pod>/episode/<int:id_ep>/edit/elab', methods=['POST'])
@login_required
def post_edit_episode(id_pod: int, id_ep: int):

    # Retriving data 
    title = request.form['title']
    desc = request.form['desc']

    # Cleaning data
    title = title.strip()
    desc = desc.strip()
    
    check = True
    if not title or not desc:
        check = False
    elif len(title) < 4 or len(title) > 32:
        check = False
    elif len(desc)<16 or len(desc) > 516:
        check = False

    # If the podcast doesnt exist or the user that is trying to edit it is not the owner abort
    episode = dao.get_episode(id_ep)
    podcast = dao.get_podcast(id_pod)
    if not episode:
        flash(message='Il podcast che hai richiesto di eliminare non esiste', category='warning')
        return redirect(session.get('previous_url', '/'))
    elif podcast['id_user'] != current_user.id: # type: ignore
        flash(message='Non sei il proprietario del podcast', category='warning')
        return redirect(url_for('episode', id_ep=id_ep, id_pod=id_pod))
    elif episode['id_podcast'] != id_pod or not podcast:
        flash(message='Podcast e episodio non corrispondono, oppure non esistono', category='warning')
        return redirect(url_for('episode', id_ep=id_ep, id_pod=id_pod))
    elif not check:
        flash(message='I dati sono mancanti o erronei, riprovare', category='warning')
        return redirect(url_for('episode', id_ep=id_ep, id_pod=id_pod))

    try:

        if episode['title'] == title:
            title = None
        if episode['description'] == desc:
            desc = None

        # Otherwise edit the podcast
        if title or desc:
            ep_result = dao.update_episode(id=id_ep, title=title, desc=desc)
        else:
            ep_result = True

        if not ep_result:
            raise dataManipulationError('Unable to update title or description')

        flash(message='Episodio modificato correttamente', category='success')
        return redirect(url_for('episode', id_ep=id_ep, id_pod=id_pod))
            
    except Exception as e:
        flash(message='C\'è stato un errore durante la modifica dell\'episodio - ERR: '+str(e), category='danger')
        return redirect(url_for('episode', id_ep=id_ep, id_pod=id_pod))

@app.route('/podcast/<int:id_pod>/episode/<int:id_ep>/audio/edit/elab', methods=['POST'])
@login_required
def post_edit_audio(id_pod, id_ep):
    
    # Retriving data 
    audio = request.files['audio']

    # Checking data
    check = True
    if not audio or not is_audio(secure_filename(audio.filename)): # type: ignore
        check = False

    # If the profile doesnt exist or the user that is trying to edit it is not the owner abort (and say it)
    podcast = dao.get_podcast(id_pod)
    episode = dao.get_episode(id_ep)

    if not podcast or not episode or not podcast['id'] == episode['id_podcast']:
        flash('L\'episodio dove hai richiesto la modifica dell\'audio non esiste', 'warning')
        return redirect(session.get('previous_url', '/'))
    elif podcast['id'] != current_user.id: # type: ignore
        flash('Non sei il propriterio del podcast', 'warning')
    elif not check:
        flash("Impossibile modificare l'audio, il file fornito non è compatibile", 'warning')
    else:
        # Otherwise save the data
        try:

            # Define filename and file extension
            filename = secure_filename(audio.filename) # type: ignore
            audioext = '.' + filename.split('.')[-1] # type: ignore
            audioname = str(id_ep) + audioext

            # Save the audio
            save_directory = AUDIOS_PATH
            if not os.path.exists(save_directory):
                os.makedirs(save_directory)
            audio.save(save_directory+audioname) # type: ignore

            # Delete old audio if it has a different extension
            if episode['audio'] != audioext:
                old_audioext = episode['audio']
                old_audioname = str(id_ep) + old_audioext
                old_file_path = save_directory + old_audioname
                if os.path.exists(old_file_path):
                    os.remove(old_file_path)

            # Update the audio extension in the db
            result = dao.update_episode(id=id_ep, audio=audioext)

            if not result:
                raise dataManipulationError('Unable to update the audio')

            flash('Audio modificato correttamente', 'success')

        # If something bad happens, abort and say it
        except Exception as e:
            flash("Impossibile aggiornare l'audio, qualcosa è andato storto - ERR: " + str(e), 'danger')

    return redirect(url_for('episode', id_ep=id_ep, id_pod=id_pod))


@app.route('/podcast/<int:id_pod>/episode/<int:id_ep>/comment/new/elab', methods=['POST'])
def post_new_comment(id_pod: int, id_ep: int):

    # Retriving data
    text = request.form['text']
    timestamp = datetime.now().strftime(ISO_TIMESTAMP)

    # Cleaning data
    text = text.strip()

    # Checking that the data is valid
    check = True
    if not text:
        check = False
    elif len(text) > 300:
        check = False

    # Retriving episode and its podcast where to put the comment
    podcast = dao.get_podcast(id_pod)
    episode = dao.get_episode(id_ep)

    # Checking that the data is valid
    checkExist = True
    if not podcast or not episode:
        checkExist = False
    elif episode['id_podcast'] != id_pod:
        checkExist = False
    
    if not check:
        flash("Impossibile aggiugere il commento, i dati iseriti sono mancanti o erronei", 'warning')
        return redirect(url_for('episode', id_pod=id_pod, id_ep=id_ep))
    elif not checkExist:
        flash("Impossibile aggiugere il commento, il podcast e/o l'episidio non esistono o non sono compatibili", 'warning')
        return redirect(session.get('previous_url', '/'))
    elif not current_user.is_authenticated: # type: ignore
        flash('Fai l\'accesso prima di aggiungere il commento', 'info')
        return redirect(url_for('episode', id_pod=id_pod, id_ep=id_ep))
    else:

        result = dao.new_comment(id_user=current_user.id, id_ep=id_ep, text=text, timestamp=timestamp)  # type: ignore

        if not result:
            flash(message='C\'è stato un errore durante l\'aggiunta del commento, riprovare', category='danger')
        return redirect(url_for('episode', id_ep=id_ep, id_pod=id_pod))

@app.route('/podcast/<int:id_pod>/episode/<int:id_ep>/comment/delete/elab', methods=['POST'])
@login_required
def post_delete_comment(id_pod: int, id_ep: int):

    timestamp = request.form['timestamp']
    
    episode = dao.get_episode(id_ep)
    podcast = dao.get_podcast(id_pod)

    comment = False
    if timestamp:
        comment = dao.get_comment(id_ep=id_ep, id_user=current_user.id, timestamp=timestamp) # type: ignore

    if not episode or not podcast or episode['id_podcast'] != id_pod:
        flash("Non puoi eliminare commenti da episodi che non esistono", category='warning')
        return redirect(session.get('previous_url', '/'))
    elif not comment:
        flash("Non puoi eliminare questo commento", category='warning')
        return redirect(url_for('episode', id_pod=id_pod, id_ep=id_ep))
    else:
        dao.delete_comment_by_PK(id_ep=id_ep, id_user=current_user.id, timestamp=timestamp) # type: ignore
        flash(message='Commento eliminato correttamente', category='success')
        return redirect(url_for('episode', id_ep=id_ep, id_pod=id_pod))

@app.route('/podcast/<int:id_pod>/episode/<int:id_ep>/comment/edit/elab', methods=['POST'])
@login_required
def post_edit_comment(id_pod: int, id_ep: int):

    # Retriving data
    text = request.form['new-text']
    id_user = current_user.id # type: ignore
    timestamp = request.form['timestamp']

    # Cleaning data
    text = text.strip()

    # Checking that the data is valid
    check = True
    if not text:
        check = False
    elif len(text) > 300:
        check = False

    # Retriving episode and its podcast where to put the comment
    podcast = dao.get_podcast(id_pod)
    episode = dao.get_episode(id_ep)

    comment = False
    if timestamp:
        comment = dao.get_comment(id_ep=id_ep, id_user=id_user, timestamp=timestamp) # type: ignore

    if not check:
        flash("Impossibile modificare il commento, i dati iseriti sono mancanti o erronei", 'warning')
        return redirect(url_for('episode', id_pod=id_pod, id_ep=id_ep))
    elif not episode or not podcast or episode['id_podcast'] != id_pod:
        flash("Non puoi modificare commenti da episodi che non esistono", category='warning')
        return redirect(session.get('previous_url', '/'))
    elif not comment:
        flash("Non puoi modificare questo commento", category='warning')
        return redirect(url_for('episode', id_pod=id_pod, id_ep=id_ep))
    else:

        result = dao.update_comment(id_user=id_user, id_ep=id_ep, new_text=text, timestamp=timestamp) # type: ignore
        if not result:
            flash(message='C\'è stato un errore durante la modifica del commento, riprovare', category='danger')

        return redirect(url_for('episode', id_ep=id_ep, id_pod=id_pod))

@app.route('/search')
def categories():
    podcasts = dao.get_podcasts()
    session['previous_url'] = request.url
    return render_template('categories.html', podcasts=podcasts)

@app.route('/random')
def random_pod():
    max_id = dao.get_last_podcast_id()
    try:
        visited_id = session['last_podcast_visited']
    except KeyError as e:
        visited_id = 0
    id = randint(1, max_id)
    while id == visited_id:
        id = randint(1, max_id)

    session['previous_url'] = request.url
    return redirect(url_for('podcast', id=id))

@app.route('/terms')
def terms():
    session['previous_url'] = request.url
    return render_template('terms.html')

@app.route('/faq')
def faq():
    session['previous_url'] = request.url
    return render_template('faq.html')

# Login manager
@login_manager.user_loader
def load_user(user_id):
    return User(dao.get_user(user_id))

# Error handling routes
@app.errorhandler(401)
def unauthorized(error):
  return render_template('error.html', error=error, code=401, previous_url=session.get('previous_url', '/'))

@app.errorhandler(403)
def forbidden(error):
  return render_template('error.html', error=error, code=403, previous_url=session.get('previous_url', '/'))

@app.errorhandler(404)
def not_found(error):
  return render_template('error.html', error=error, code=404, previous_url=session.get('previous_url', '/'))

@app.errorhandler(405)
def handle_method_not_allowed(error):
    return render_template('error.html', error=error, code=405, previous_url=session.get('previous_url', '/'))

# Route for testing pages (ignore this)
@app.route('/test')
def test():
    return render_template('error.html')

# Route for cleaning data stoared by Flask-Session and Flask-Login
@app.route('/clear_session')
def clear_session():
    session.clear()
    return 'Session data cleared!'

@app.route('/clear_login')
def clear_login():
    logout_user()
    return 'Login data cleared!'