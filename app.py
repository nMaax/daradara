# Vanilla Python libraries
import os, re, secrets, sqlite3
from datetime import datetime, date, timedelta
from dateutil import parser as date_parser


# Personal libraries
import data.dao as dao
from data.errors.daoExceptions import dataManipulationError, notPodcastOwnerError
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

DEFAULT_HOUR = "00:00:01"
ISO_DATE = "%Y-%m-%d"
ISO_TIMESTAMP = "%Y-%m-%d %H:%M:%S"

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

    # Retrieve the user from the database using dao
    user = dao.get_user_by_email(email)

    # Check if the user exists and the password is correct
    if user and check_password_hash(user['password'], password): #TODO check_password_hash(user.get('password'), password):
        # Login the user using Flask-Login's login_user function
        #TODO Imposta remeber in base alla checkbox remember me, metti duration a un valore più normale, non per il debug
        if remember:
            login_user(User(user), remember=True, duration=LOGIN_MAX_DURATION)
        else:
            login_user(User(user), remember=False, duration=LOGIN_MAX_DURATION)
        # Return a success message if the login works
        flash(message='Login effettuato con successo!', category='success')
        return redirect(url_for('index'))
    else:
        # Return an error message if the login fails
        flash('Email e password non corretti, riprovare', 'warning')
        return redirect(url_for('login'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout effettuato', 'success')
    return redirect(url_for('index'))

@app.route('/profile/<int:id>')
def profile(id):
    user = dao.get_user(id)
    creators = dao.get_creators()
    is_creator = False
    if user and creators:
        podcasts = dao.get_podcasts_by_user(id_user=id)
        follows = dao.get_follows_join_podcasts(id_user=id)
        saves = dao.get_saves_join_episodes_podcasts(id_user=id)
        for creator in creators:
            if creator['id'] == user['id']:
                is_creator = True
        return render_template('profile.html', user=user, podcasts=podcasts, follows=follows, saves=saves, is_creator = is_creator)
    else:
        flash(message='L\'utente cercato non esiste', category='warning')
        return redirect(url_for('index'))
    

#TODO Trim and capitalize in order to don't have duplicates
@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup/elab', methods=['POST'])
def post_signup():

    #TODO! con js controlla che le lunghezze dei campi siano giuste senza gli whitespace
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
    elif len(password) < 8: #TODO! Controlla che vengano inseriti tutti i caratteri speciali
        check = False
    elif not is_image(secure_filename(propic.filename)): # type: ignore
        check = False

    # If the data isn't correct say it, otherwhise continue 
    if not check:
        flash("Dati inseriti mancanti o erronei, riprovare", 'warning')
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
            save_directory = 'static/uploads/images/propics/'
            if not os.path.exists(save_directory):
                os.makedirs(save_directory)
            propic.save(save_directory+propicname) # type: ignore
            
            # Automatic login after registration
            login_user(User(dao.get_user_by_email(email)), remember=False)
            
            flash("Utente registrato correttamente!", 'success')
            return redirect(url_for('profile', id=user_id)) # type: ignore
        except Exception as e:
            flash("Impossibile registrare il nuovo utente, qualcosa è andato storto - ERR: " + str(e), 'danger')
            return redirect(url_for('signup'))

        
@app.route('/podcast/<int:id>')
def podcast(id):
    podcast = dao.get_podcast(id)
    episodes = dao.get_episodes(id_podcast = id)
    category = dao.get_category(id)

    if podcast:
        return render_template('podcast.html', id=id, podcast = podcast, episodes = episodes, category = category)
    else:
        flash(message='Il podcast cercato non esiste', category='warning')
        return redirect(url_for('index'))

@app.route('/podcast/new')
def new_podcast():
    if not current_user.is_authenticated: # type: ignore
        flash('Devi aver fatto l\'accesso prima di poter creare un podcast', category='warning')
        return redirect(url_for('index'))
    else:
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
    desc = desc.strip()
    category = category.strip()
    category = category.lower()
    
    #TODO! Check, via javascript, in the form that the max-min lengt is in the range ignoring whitespaces: ask to chatGPT how to do it
    check = True
    if not title or not desc or not img or not category:
        check = False
    elif len(title) < 4 or len(title) > 32:
        check = False
    elif dao.get_podcast_by_title(title):
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
    else:
        # Retrive the id of the creator and the id the podcast will have
        user_id = current_user.id # type: ignore
        podcast_id = dao.get_last_podcast_id() + 1

        # Define image name
        filename = secure_filename(img.filename) # type: ignore
        imgext = '.' + filename.split('.')[-1] # type: ignore
        imgname = str(podcast_id) + imgext

        # If dao is unable to insert data, abort and do not save the image
        try:
            # Inserting entry in the database
            result = dao.new_podcast(title, desc, imgext, user_id, category)

            #TODO! con javascript controlla che non ci sia già un podcast con quel titolo
            if not result:
                raise dataManipulationError('Unable to add entry into the database')

            # Save the image (only if the podcast has been saved)
            save_directory = 'static/uploads/images/covers/'
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
def post_delete_podcast(id):

    # If the podcast doesnt exist or the user that is trying to delete it is not the owner abort
    podcast = dao.get_podcast(id)
    if not podcast:
        flash(message='Il podcast che hai richiesto di eliminare non esiste', category='warning')
        return redirect(url_for('index'))
    elif podcast['id_user'] != current_user.id: # type: ignore
        flash(message='Non sei il proprietario del podcast', category='warning')
        return redirect(url_for('podcast', id=id))

    # Otherwise delete the podcast (and its image)
    result = dao.delete_podcast(id)
    if result:
        #path = os.path.join(app.root_path, url_for('static', filename='uploads/images/covers/'+str(podcast['id'])+podcast['img']))
        file_path = 'static/uploads/images/covers/'+str(podcast['id'])+podcast['img']
        abs_path = os.path.abspath(file_path)
        os.remove(abs_path)
        flash(message='Podcast eliminato correttamente', category='success')
    else:
        flash(message='C\'è stato un errore durante l\'eliminazione del podcast, riprovare', category='danger')
    return redirect(url_for('index'))

@app.route('/podcast/<int:id>/edit/elab', methods=['POST'])
@login_required
def post_edit_podcast(id):

    # Retriving data 
    title = request.form['title']
    desc = request.form['desc']
    category = request.form['category']

    # Cleaning data
    title = title.strip()
    desc = desc.strip()
    category = category.strip()
    category = category.lower()
    
    #TODO! Check, via javascript, in the form that the max-min lengt is in the range ignoring whitespaces: ask to chatGPT how to do it
    check = True
    if not title or not desc or not category:
        check = False
    elif len(title) < 4 or len(title) > 32:
        check = False
    elif len(desc)<16 or len(desc) > 516:
        check = False
    elif len(category) < 4 or len(category) > 32:
        check = False

    # If the podcast doesnt exist or the user that is trying to edit it is not the owner abort
    podcast = dao.get_podcast_with_tags(id)
    if not podcast:
        flash(message='Il podcast che hai richiesto di eliminare non esiste', category='warning')
        return redirect(url_for('index'))
    elif podcast['id_user'] != current_user.id: # type: ignore
        flash(message='Non sei il proprietario del podcast', category='warning')
        return redirect(url_for('podcast', id=id))
    elif not check:
        flash(message='I dati sono mancanti o erronei, riprovare', category='warning')
        return redirect(url_for('podcast', id=id))

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
            tag_result = dao.update_tag(id_pod=id, tag=category)
        else:
            tag_result = True

        if not pod_result:
            raise dataManipulationError('Unable to update title or description')
        elif not tag_result:
            raise dataManipulationError('Unable to update category')

        flash(message='Podcast modificato correttamente', category='success')
        return redirect(url_for('podcast', id=id))
            
    except Exception as e:
        flash(message='C\'è stato un errore durante la modifica del podcast - ERR: '+str(e), category='danger')
        return redirect(url_for('podcast', id=id))

@app.route('/podcast/<int:id>/img/edit/elab', methods=['POST'])
def post_update_podcast_img(id):

    img = request.files['img']

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

            filename = secure_filename(img.filename) # type: ignore
            imgext = '.' + filename.split('.')[-1] # type: ignore
            imgname = str(id) + imgext

            # Save the image (only if the podcast has been saved)
            save_directory = 'static/uploads/images/covers/'
            if not os.path.exists(save_directory):
                os.makedirs(save_directory)
            img.save(save_directory+imgname) # type: ignore

            result = dao.update_podcast(id, img=imgext)

            if not result:
                raise dataManipulationError('Unable to update the image')

            flash('Immagine modificata correttamente', 'success')

        except Exception as e:
            flash("Impossibile aggiornare l'immagine, qualcosa è andato storto - ERR: " + str(e), 'danger')

    return redirect(url_for('podcast', id=id))

@app.route('/podcast/<int:id_pod>/episode/<int:id_ep>')
def episode(id_pod, id_ep):
    episode = dao.get_episode(id_ep)
    if episode and episode['id_podcast'] == id_pod:
        podcast = dao.get_podcast(id_pod)
        comments = dao.get_comments_extended(id_ep)
        if comments:
            n_comments = len(comments)
        else:
            n_comments = 0
        return render_template('episode.html', id=id_ep, id_pod=id_pod, podcast=podcast, episode=episode, comments=comments, n_comments = n_comments)
    else:
        flash(message='L\'episodio che hai provato di aprire non appartiene a questo podcast', category='warning')
        return redirect(url_for('index'))

@app.route('/podcast/<int:id_pod>/episode/new')
@login_required
def new_episode(id_pod):
    podcast = dao.get_podcast(id_pod)
    if not podcast:
        flash('Il podcast nel quale hai cercato di creare l\'episodio non esiste', 'warning')
        return redirect(url_for('index'))
    elif podcast['id_user'] != current_user.id: # type: ignore
        flash('Non sei il proprietario del podcast', 'warning')
        return redirect(url_for('podcast', id=id_pod))
    else:
        return render_template('new-episode.html', id_pod=id_pod, podcast=podcast)

@app.route('/podcast/<int:id_pod>/episode/new/elab', methods=['POST'])
@login_required
def post_new_episode(id_pod):
    
    # Retriving data
    title = request.form['title']
    desc = request.form['desc']
    audio = request.files['audio']
    date = request.form['date']

    # Cleaning data
    title = title.strip()
    desc = desc.strip()
    
    #TODO! Check, via javascript, in the form that the max-min lengt is in the range ignoring whitespaces: ask to chatGPT how to do it
    #TODO! con javascript controlla che non ci sia già un podcast con quel titolo
    # Checking that the data is valid
    check = True
    if not title or not desc or not audio:
        check = False
    elif len(title) < 4 or len(title) > 32:
        check = False
    elif dao.get_episode_by_title(title=title, id_pod=id_pod):
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
        elif py_date.date() > max_date.date(): #TODO! Controlla con js che la data non vada oltre oggi
            raise ValueError("The date is before the date lower bound")

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
            save_directory = 'static/uploads/audios/'
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
def post_delete_episode(id_pod, id_ep):
    episode = dao.get_episode(id_ep)
    podcast = dao.get_podcast(id_pod)

    if not episode or not podcast:
        flash('L\'episodio che hai richiesto di eliminare non esiste', category='warning')
        return redirect(url_for('index'))
    elif episode['id_podcast'] != id_pod:
        flash('L\'episodio e il podcast nell\'url non corrispondono', category='warning')
        return redirect(url_for('index'))
    elif podcast['id_user'] != current_user.id: # type: ignore
        flash('Non sei il proprietario del podcast', category='warning')
        return redirect(url_for('episode', id_pod=id_pod, id_ep=id_ep))
    else:
        result = dao.delete_episode(id_ep)
        if result:
            #TODO! in cascata devi eliminare anche tutti gli audio
            #path = os.path.join(app.root_path, url_for('static', filename='uploads/audios/'+str(episode['id'])+episode['img']))
            file_path = 'static/uploads/audios/'+str(episode['id'])+episode['audio']
            abs_path = os.path.abspath(file_path)
            os.remove(abs_path)
            flash(message='Episodio eliminato correttamente', category='success')
            return redirect(url_for('podcast', id=id_pod))
        else:
            flash(message='C\'è stato un errore durante l\'eliminazione dell\'episodio, riporvare', category='danger')
            return redirect(url_for('episode', id_pod=id_pod, id_ep=id_ep))

@app.route('/podcast/<int:id_pod>/episode/<int:id_ep>/edit/elab', methods=['POST'])
@login_required
def post_edit_episode(id_pod, id_ep):

    # Retriving data 
    title = request.form['title']
    desc = request.form['desc']

    # Cleaning data
    title = title.strip()
    desc = desc.strip()
    
    #TODO! Check, via javascript, in the form that the max-min lengt is in the range ignoring whitespaces: ask to chatGPT how to do it
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
        return redirect(url_for('index'))
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

@app.route('/podcast/<int:id_pod>/episode/<int:id_ep>/comment/new/elab', methods=['POST'])
def post_new_comment(id_pod, id_ep):

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
        return redirect(url_for('index'))
    elif not current_user.is_authenticated: # type: ignore
        flash("Fare il login prima di aggiungere il commento", 'warning')
        return redirect(url_for('episode', id_pod=id_pod, id_ep=id_ep))
    else:

        result = dao.new_comment(id_user=current_user.id, id_ep=id_ep, text=text, timestamp=timestamp)  # type: ignore

        if not result:
            flash(message='C\'è stato un errore durante l\'aggiunta del commento, riprovare', category='danger')
        return redirect(url_for('episode', id_ep=id_ep, id_pod=id_pod))

@app.route('/podcast/<int:id_pod>/episode/<int:id_ep>/comment/delete/elab', methods=['POST'])
@login_required
def post_delete_comment(id_pod, id_ep):

    timestamp = request.form['timestamp']
    
    episode = dao.get_episode(id_ep)
    podcast = dao.get_podcast(id_pod)

    comment = False
    if timestamp:
        comment = dao.get_comment(id_ep=id_ep, id_user=current_user.id, timestamp=timestamp) # type: ignore

    if not episode or not podcast or episode['id_podcast'] != id_pod:
        flash("Non puoi eliminare commenti da episodi che non esistono", category='warning')
        return redirect(url_for('index'))
    elif not comment:
        flash("Non puoi eliminare questo commento", category='warning')
        return redirect(url_for('episode', id_pod=id_pod, id_ep=id_ep))
    else:
        dao.delete_comment_by_PK(id_ep=id_ep, id_user=current_user.id, timestamp=timestamp) # type: ignore
        flash(message='Commento eliminato correttamente', category='success')
        return redirect(url_for('episode', id_ep=id_ep, id_pod=id_pod))

@app.route('/podcast/<int:id_pod>/episode/<int:id_ep>/comment/edit/elab', methods=['POST'])
@login_required
def post_edit_comment(id_pod, id_ep):

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
        return redirect(url_for('index'))
    elif not comment:
        flash("Non puoi modificare questo commento", category='warning')
        return redirect(url_for('episode', id_pod=id_pod, id_ep=id_ep))
    else:

        result = dao.update_comment(id_user=id_user, id_ep=id_ep, new_text=text, timestamp=timestamp) # type: ignore
        if not result:
            flash(message='C\'è stato un errore durante la modifica del commento, riprovare', category='danger')

        return redirect(url_for('episode', id_ep=id_ep, id_pod=id_pod))

# Login manager
@login_manager.user_loader
def load_user(user_id):
    return User(dao.get_user(user_id))

# Error handling routes
@app.errorhandler(401)
def unauthorized(error):
  return render_template('401.html', error=error)

@app.errorhandler(403)
def forbidden(error):
  return render_template('403.html', error=error)

@app.errorhandler(404)
def not_found(error):
  return render_template('404.html', error=error)

# Route for testing pages (ignore this)
@app.route('/test')
def test():
    flash(message='Messaggio', category='dark')
    return render_template('test.html')

# Route for cleaning data stoared by Flask-Session and Flask-Login
@app.route('/clear_session')
def clear_session():
    session.clear()
    return 'Session data cleared!'

@app.route('/clear_login')
def clear_login():
    logout_user()
    return 'Login data cleared!'