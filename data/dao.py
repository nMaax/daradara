import sqlite3
import os
from data.errors.daoExceptions import dataManipulationError

FILENAME = 'data.db'
SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
PATH = os.path.join(SCRIPT_DIR, FILENAME)

ISO_TIMESTAMP = "%Y-%m-%d %H:%M:%S"

# SELECT queries

def get_priv_owned(id_user):
    conn, cursor = connect()
    priv_owned = None

    try:
        sql = 'SELECT priv_owned FROM users WHERE id = ?'
        cursor.execute(sql, (id_user,))
        priv_owned = cursor.fetchone()
        if priv_owned and priv_owned['priv_owned'] == 1:
            priv_owned = True
        elif priv_owned and priv_owned['priv_owned'] == 0:
            priv_owned = False
        else:
            priv_owned = None
    except Exception as e:
        print(e)

    close(conn, cursor)
    return priv_owned

def get_priv_follows(id_user):
    conn, cursor = connect()
    priv_follows = None

    try:
        sql = 'SELECT priv_follows FROM users WHERE id = ?'
        cursor.execute(sql, (id_user,))
        priv_follows = cursor.fetchone()
        if priv_follows and priv_follows['priv_follows'] == 1:
            priv_follows = True
        elif priv_follows and priv_follows['priv_follows'] == 0:
            priv_follows = False
        else:
            priv_follows = None
    except Exception as e:
        print(e)

    close(conn, cursor)
    return priv_follows

def get_priv_saves(id_user):
    conn, cursor = connect()
    priv_saves = None

    try:
        sql = 'SELECT priv_saves FROM users WHERE id = ?'
        cursor.execute(sql, (id_user,))
        priv_saves = cursor.fetchone()
        if priv_saves and priv_saves['priv_saves'] == 1:
            priv_saves = True
        elif priv_saves and priv_saves['priv_saves'] == 0:
            priv_saves = False
        else:
            priv_saves = None
    except Exception as e:
        print(e)

    close(conn, cursor)
    return priv_saves

def has_saved(id_user, id_ep):
    conn, cursor = connect()
    has_saved = False

    try:
        sql = 'SELECT * FROM saves WHERE id_ep = ? AND id_user = ?'
        cursor.execute(sql, (id_ep, id_user))
        saves = cursor.fetchone()
        if saves:
            has_saved = True
    except Exception as e:
        print(e)

    close(conn, cursor)
    return has_saved

def get_saves_join_episodes_podcasts(id_user):
    conn, cursor = connect()
    saves = []

    try:
        sql = 'SELECT podcasts.id AS "id", episodes.id AS "ep_id", episodes.title AS "title", episodes.description "desc", podcasts.img AS "img", podcasts.title AS "podcast_title" FROM saves, episodes, podcasts WHERE saves.id_ep = episodes.id AND episodes.id_podcast = podcasts.id AND saves.id_user = ? ORDER BY saves.timestamp DESC'
        cursor.execute(sql, (id_user,))
        saves = cursor.fetchall()
    except Exception as e:
        print(e)

    close(conn, cursor)
    return saves

def get_saves(id_user):
    conn, cursor = connect()
    saves = []

    try:
        sql = 'SELECT * FROM saves WHERE id_user = ?'
        cursor.execute(sql, (id_user,))
        saves = cursor.fetchall()
    except Exception as e:
        print(e)

    close(conn, cursor)
    return saves

def is_following(id_user, id_pod):
    conn, cursor = connect()
    is_following = False

    try:
        sql = 'SELECT * FROM follows WHERE id_podcast = ? AND id_user = ?'
        cursor.execute(sql, (id_pod, id_user))
        follows = cursor.fetchone()
        if follows:
            is_following = True
    except Exception as e:
        print(e)

    close(conn, cursor)
    return is_following

def get_follows_join_podcasts(id_user):
    conn, cursor = connect()
    follows = []

    try:
        # Nonostante non vi siano altre collonne che si chiamino 'id_user' COMUNQUE sqlite vuole che si tolga ambiguità con follows.id_user invece di id_user e basta, uffi :(
        sql = 'SELECT * FROM follows, podcasts WHERE follows.id_podcast = podcasts.id AND follows.id_user = ? ORDER BY follows.timestamp DESC'
        cursor.execute(sql, (id_user,))
        follows = cursor.fetchall()
    except Exception as e:
        print(e)

    close(conn, cursor)
    return follows

def get_follows(id_user):
    conn, cursor = connect()
    follows = []

    try:
        sql = 'SELECT * FROM follows WHERE id_user = ? ORDER BY timestamp DESC'
        cursor.execute(sql, (id_user,))
        follows = cursor.fetchall()
    except Exception as e:
        print(e)

    close(conn, cursor)
    return follows

def get_category(id_podcast):
    conn, cursor = connect()
    category = None

    try:
        sql = 'SELECT category FROM podcasts WHERE id = ?'
        cursor.execute(sql, (id_podcast,))
        category = cursor.fetchone()
    except Exception as e:
        print(e)

    close(conn, cursor)
    return category

def get_comments_join_users(id_ep):
    conn, cursor = connect()
    comments = []
    
    try:
        sql = 'SELECT comments.id_user, text, timestamp, name, surname, email, propic FROM comments, users WHERE comments.id_user = users.id AND id_ep = ? ORDER BY timestamp DESC'
        cursor.execute(sql, (id_ep,))
        comments = cursor.fetchall()
    except Exception as e:
        print(e)

    close(conn, cursor)
    return comments

def get_comments(id_ep=None, id_user=None):
    conn, cursor = connect()
    comments = []
    data = None

    sql = 'SELECT * FROM comments'
    if id_ep is not None and id_user is not None:
        sql += ' WHERE id_ep = ? AND id_user = ?'
        data = (id_ep, id_user)
    elif id_ep is not None and id_user is None:
        sql += ' WHERE id_ep = ?'
        data = (id_ep,)
    elif id_ep is None and id_user is not None:
        sql += ' WHERE id_user = ?'
        data = (id_user,)
    
    try:
        if data is not None:
            cursor.execute(sql, data)
        else:
            cursor.execute(sql)
        comments = cursor.fetchall()
    except Exception as e:
        print(e)

    close(conn, cursor)
    return comments

def get_comment(id_ep, id_user, timestamp):
    conn, cursor = connect()
    comment = None

    try:
        sql = 'SELECT * FROM comments WHERE id_ep = ? AND id_user = ? AND timestamp = ?'
        cursor.execute(sql, (id_ep, id_user, timestamp))
        comment = cursor.fetchone()
    except Exception as e:
        print(e)

    close(conn, cursor)
    return comment

def get_episodes(id_podcast):
    conn, cursor = connect()
    episodes = []

    try:
        sql = 'SELECT * FROM episodes WHERE id_podcast = ? ORDER BY timestamp DESC'
        cursor.execute(sql, (id_podcast,))
        episodes = cursor.fetchall()
    except Exception as e:
        print(e)

    close(conn, cursor)
    return episodes

def get_episode_by_title(title, id_pod):
    conn, cursor = connect()
    episode = None

    try:
        sql = 'SELECT * FROM episodes WHERE title = ? AND id_podcast = ?'
        cursor.execute(sql, (title, id_pod))
        episode = cursor.fetchone()
    except Exception as e:
        print(e)

    close(conn, cursor)
    return episode

def get_last_episode_id():
    conn, cursor = connect()
    id = 0

    try:
        sql = "SELECT seq FROM sqlite_sequence WHERE name = 'episodes'"
        cursor.execute(sql)
        id = cursor.fetchone()['seq']
        if id == None:
            id = 0
    except Exception as e:
        print(e)

    close(conn, cursor)
    return id

def get_episode(id):
    conn, cursor = connect()
    episode = None

    try:
        sql = 'SELECT * FROM episodes WHERE id = ?'
        cursor.execute(sql, (id,))
        episode = cursor.fetchone()
    except Exception as e:
        print(e)

    close(conn, cursor)
    return episode

def get_creators():
    conn, cursor = connect()
    user = []

    try:
        sql = 'SELECT users.* FROM users, podcasts WHERE users.id = podcasts.id_user'
        cursor.execute(sql)
        user = cursor.fetchall()
    except Exception as e:
        print(e)

    close(conn, cursor)    
    return user

def get_users():
    users = []
    for id in range(1, get_last_id_user() + 1):
        user = get_user(id)
        if user:
            users.append(user)
    return users

def get_user_by_email(email):
    conn, cursor = connect()
    user = None

    try:
        sql = 'SELECT * FROM users WHERE email = ?'
        cursor.execute(sql, (email,))
        user = cursor.fetchone()
    except Exception as e:
        print(e)

    close(conn, cursor)    
    return user

def get_user(id):
    conn, cursor = connect()
    user = None

    try:
        sql = 'SELECT * FROM users WHERE id = ?'
        cursor.execute(sql, (id,))
        user = cursor.fetchone()
    except Exception as e:
        print(e)

    close(conn, cursor)    
    return user

def get_last_id_user():
    conn, cursor = connect()
    id = 0

    try:
        sql = "SELECT seq FROM sqlite_sequence WHERE name = 'users'"
        cursor.execute(sql)
        id = cursor.fetchone()['seq']
        if id == None:
            id = 0
    except Exception as e:
        print(e)

    close(conn, cursor)    
    return id

def get_podcast_extended(id_podcast):
    conn, cursor = connect()
    podcast = None

    try:
        sql = 'SELECT * FROM podcasts, users, episodes WHERE podcasts.id_user = users.id AND episodes.id_podcast = podcasts.id AND id_podcast = ? ORDER BY podcasts.id, episodes.id ASC'
        cursor.execute(sql, (id_podcast,))
        podcast = cursor.fetchall()
    except Exception as e:
        print(e)

    close(conn, cursor)
    return podcast

def get_last_update(id_pod):
    conn, cursor = connect()
    timestamp = None

    try:
        sql = "SELECT MAX(timestamp) as 'last_update' FROM podcasts, episodes WHERE podcasts.id = episodes.id_podcast AND podcasts.id = ?"
        cursor.execute(sql, (id_pod,))
        timestamp = cursor.fetchone()
    except Exception as e:
        print(e)

    close(conn, cursor)
    return timestamp

def get_podcasts_onfire(number_of_podcasts=5):
    conn, cursor = connect()
    podcasts = []

    try:
        sql = 'SELECT podcasts.id, COUNT(follows.id_user) AS "n_follows", last_update, last_updates.timestamp, podcasts.title, podcasts.desc, podcasts.img FROM podcasts, follows, (SELECT podcasts.id AS "id_podcast_lu", MAX(timestamp) AS "last_update", MAX(timestamp) AS "timestamp" FROM podcasts, episodes WHERE podcasts.id = episodes.id_podcast GROUP BY podcasts.id) AS "last_updates"WHERE podcasts.id = follows.id_podcast AND last_updates.id_podcast_lu = podcasts.id GROUP BY podcasts.id ORDER BY n_follows DESC'
        cursor.execute(sql)
        podcasts = cursor.fetchmany(size=number_of_podcasts)
    except Exception as e:
        print(e)

    close(conn, cursor)
    return podcasts

def get_podcasts():
    podcasts = []
    for id in range(1, get_last_podcast_id() + 1 ):
        podcast = get_podcast(id)
        if podcast:
            podcasts.append(podcast)
    return podcasts

def get_podcasts_by_user(id_user):
    conn, cursor = connect()
    podcast = []

    try:
        sql = 'SELECT * FROM podcasts WHERE id_user = ?'
        cursor.execute(sql, (id_user,))
        podcast = cursor.fetchall()
    except Exception as e:
        print(e)

    close(conn, cursor)
    return podcast

def get_podcast_by_title(title):
    conn, cursor = connect()
    podcast = None

    try:
        sql = 'SELECT * FROM podcasts WHERE title = ?'
        cursor.execute(sql, (title,))
        podcast = cursor.fetchone()
    except Exception as e:
        print(e)

    close(conn, cursor)
    return podcast

def get_podcast(id):
    conn, cursor = connect()
    podcast = None

    try:
        sql = 'SELECT * FROM podcasts WHERE id = ?'
        cursor.execute(sql, (id,))
        podcast = cursor.fetchone()
    except Exception as e:
        print(e)

    close(conn, cursor)
    return podcast

def get_last_podcast_id():
    conn, cursor = connect()
    id = 0

    try:
        sql = "SELECT seq FROM sqlite_sequence WHERE name = 'podcasts'"
        cursor.execute(sql)
        id = cursor.fetchone()['seq']
        if id == None:
            id = 0
    except Exception as e:
        print(e)

    close(conn, cursor)
    return id

# INSERT queries

def follow(id_pod, id_user, timestamp):
    conn, cursor = connect()
    success = True

    try:
        sql = 'INSERT INTO follows(id_user, id_podcast, timestamp) VALUES (?, ?, ?) '
        cursor.execute(sql, (id_user, id_pod, timestamp))
        conn.commit()
    except Exception as e:
        success = False
        print(e)
        conn.rollback()

    close(conn, cursor)
    return success

def save(id_ep, id_user, timestamp):
    conn, cursor = connect()
    success = True

    try:
        sql = 'INSERT INTO saves(id_user, id_ep, timestamp) VALUES (?, ?, ?) '
        cursor.execute(sql, (id_user, id_ep, timestamp))
        conn.commit()
    except Exception as e:
        success = False
        print(e)
        conn.rollback()

    close(conn, cursor)
    return success

def new_follow(id_user, id_podcast, timestamp):
    conn, cursor = connect()
    success = True

    try:
        sql = 'INSERT INTO follows(id_user, id_podcast, timestamp) VALUES (?, ?, ?)'
        cursor.execute(sql, (id_user, id_podcast, timestamp))
        conn.commit()
    except Exception as e:
        success = False
        print(e)
        conn.rollback()

    close(conn, cursor)
    return success

def new_save(id_user, id_ep, timestamp):
    conn, cursor = connect()
    success = True

    try:
        sql = 'INSERT INTO saves(id_user, id_ep, timestamp) VALUES (?, ?, ?)'
        cursor.execute(sql, (id_user, id_ep, timestamp))
        conn.commit()
    except Exception as e:
        success = False
        print(e)
        conn.rollback()

    close(conn, cursor)
    return success

def new_comment(id_user, id_ep, text, timestamp):
    conn, cursor = connect()
    success = True

    try:
        sql = 'INSERT INTO comments(id_user, id_ep, text, timestamp) VALUES (?, ?, ?, ?)'
        cursor.execute(sql, (id_user, id_ep, text, timestamp))
        conn.commit()
    except Exception as e:
        success = False
        print(e)
        conn.rollback()

    close(conn, cursor)
    return success

def new_episode(title, description, audio, timestamp, id_podcast):
    conn, cursor = connect()
    success = True

    try:
        sql = 'INSERT INTO episodes(title, description, audio, timestamp, id_podcast) VALUES (?, ?, ?, ?, ?)'
        cursor.execute(sql, (title, description, audio, timestamp, id_podcast))
        conn.commit()
    except Exception as e:
        success = False
        print(e)
        conn.rollback()

    close(conn, cursor)
    return success

def new_podcast(title, description, img, id_user, category):
    conn, cursor = connect()
    success = True

    try:
        sql = 'INSERT INTO podcasts(title, desc, img, category, id_user) VALUES (?, ?, ?, ?, ?)'
        cursor.execute(sql, (title, description, img, category, id_user))

        conn.commit()
    except Exception as e_pod:
        success = False
        print(e_pod)
        conn.rollback()

    close(conn, cursor)
    return success

def new_user(email, password, name, surname, propic):
    conn, cursor = connect()
    success = True

    try:
        sql = 'INSERT INTO users(email, password, name, surname, propic) VALUES (?, ?, ?, ?, ?)'
        cursor.execute(sql, (email, password, name, surname, propic))
        conn.commit()
    except Exception as e:
        success = False
        print(e)
        conn.rollback()

    close(conn, cursor)
    return success

# UPDATE queries

def switch_priv_owned(id):
    conn, cursor = connect()
    success = True

    try:
        current_value = get_priv_owned(id)
        if current_value:
            value = 0
        else:
            value = 1
        sql = 'UPDATE users SET priv_owned = ? WHERE id = ?'
        cursor.execute(sql, (value, id))
        conn.commit()
    except Exception as e:
        success = False
        print(e)
        conn.rollback()

    close(conn, cursor)
    return success

def switch_priv_follows(id):
    conn, cursor = connect()
    success = True

    try:
        current_value = get_priv_follows(id)
        if current_value:
            value = 0
        else:
            value = 1
        sql = 'UPDATE users SET priv_follows = ? WHERE id = ?'
        cursor.execute(sql, (value, id))
        conn.commit()
    except Exception as e:
        success = False
        print(e)
        conn.rollback()

    close(conn, cursor)
    return success

def switch_priv_saves(id):
    conn, cursor = connect()
    success = True

    try:
        current_value = get_priv_saves(id)
        if current_value:
            value = 0
        else:
            value = 1
        sql = 'UPDATE users SET priv_saves = ? WHERE id = ?'
        cursor.execute(sql, (value, id))
        conn.commit()
    except Exception as e:
        success = False
        print(e)
        conn.rollback()

    close(conn, cursor)
    return success

def update_category(id_pod, category):
    conn, cursor = connect()
    success = True

    try:
        sql = 'UPDATE podcasts SET category = ? WHERE id = ?'
        cursor.execute(sql, (category, id_pod))
        conn.commit()
    except Exception as e:
        success = False
        print(e)
        conn.rollback()

    close(conn, cursor)
    return success

def update_comment(id_user, id_ep, new_text, timestamp):
    conn, cursor = connect()
    success = True

    try:
        sql = 'UPDATE comments SET text = ? WHERE id_user = ? AND id_ep = ? AND timestamp = ?'
        cursor.execute(sql, (new_text, id_user, id_ep, timestamp))
        conn.commit()
    except Exception as e:
        success = False
        print(e)
        conn.rollback()

    close(conn, cursor)
    return success

def update_episode(id, title=None, desc=None, audio=None, timestamp=None):
    success = False
    if title is not None:
        success = update_episode_field(id, 'title', title)
    if desc is not None:
        success = update_episode_field(id, 'description', desc)
    if audio is not None:
        success = update_episode_field(id, 'audio', audio)
    if timestamp is not None:
        success = update_episode_field(id, 'timestamp', timestamp)
    return success

def update_episode_field(id, field, value):
    conn, cursor = connect()
    success = True

    try:
        if field == 'title' or field == 'description' or field == 'timestamp' or field == 'audio':
            sql = 'UPDATE episodes SET '+ field +' = ? WHERE id = ?'
        else:
            raise ValueError('Invalid field name')

        cursor.execute(sql, (value, id))
        conn.commit()
    except Exception as e:
        success = False
        print(e)
        conn.rollback()

    close(conn, cursor)
    return success

def update_podcast(id, title=None, desc=None, img=None):
    success = False
    if title is not None:
        success = update_podcast_field(id, 'title', title)
    if desc is not None:
        success = update_podcast_field(id, 'desc', desc)
    if img is not None:
        success = update_podcast_field(id, 'img', img)
    return success

def update_podcast_field(id, field, value):
    conn, cursor = connect()
    success = True

    try:
        if field == 'title' or field == 'desc' or field == 'img':
            sql = 'UPDATE podcasts SET '+ field +' = ? WHERE id = ?'
        else:
            raise ValueError('Invalid field name')

        cursor.execute(sql, (value, id))
        conn.commit()
    except Exception as e:
        success = False
        print(e)
        conn.rollback()

    close(conn, cursor)
    return success

def update_user_bio(id, bio):
    conn, cursor = connect()
    success = True

    try:
        sql = 'UPDATE users SET bio = ? WHERE id = ?'

        cursor.execute(sql, (bio, id))
        conn.commit()
    except Exception as e:
        success = False
        print(e)
        conn.rollback()

    close(conn, cursor)
    return success

def update_user_img(id, img):
    conn, cursor = connect()
    success = True

    try:
        sql = 'UPDATE users SET propic = ? WHERE id = ?'
        cursor.execute(sql, (img, id))
        conn.commit()
    except Exception as e:
        success = False
        print(e)
        conn.rollback()

    close(conn, cursor)
    return success

# DELETE queries

def unfollow(id_pod, id_user):
    conn, cursor = connect()
    success = True

    try:
        sql = 'DELETE FROM follows WHERE id_user = ? AND id_podcast = ?'
        cursor.execute(sql, (id_user, id_pod))
        conn.commit()
    except Exception as e:
        success = False
        print(e)
        conn.rollback()

    close(conn, cursor)
    return success

def unsave(id_ep, id_user):
    conn, cursor = connect()
    success = True

    try:
        sql = 'DELETE FROM saves WHERE id_user = ? AND id_ep = ?'
        cursor.execute(sql, (id_user, id_ep))
        conn.commit()
    except Exception as e:
        success = False
        print(e)
        conn.rollback()

    close(conn, cursor)
    return success

def delete_comment_by_PK(id_ep, id_user, timestamp):
    conn, cursor = connect()
    success = True

    try:
        sql = 'DELETE FROM comments WHERE id_ep = ? AND id_user = ? AND timestamp = ?'
        cursor.execute(sql, (id_ep, id_user, timestamp))
        conn.commit()
    except Exception as e:
        success = False
        print(e)
        conn.rollback()

    close(conn, cursor)
    return success

def delete_comment(id_ep=None, id_user=None):
    conn, cursor = connect()
    success = True
    data = None

    sql = 'DELETE FROM comments'
    if id_ep is not None and id_user is not None:
        sql += ' WHERE id_ep = ? AND id_user = ?'
        data = (id_ep, id_user)
    elif id_ep is not None and id_user is None:
        sql += ' WHERE id_ep = ?'
        data = (id_ep,)
    elif id_ep is None and id_user is not None:
        sql += ' WHERE id_user = ?'
        data = (id_user,)

    try:
        if data is not None:
            cursor.execute(sql, data)
        else:
            cursor.execute(sql)

        conn.commit()
    except Exception as e:
        success = False
        print(e)
        conn.rollback()

    close(conn, cursor)
    return success

def delete_episode(id):
    conn, cursor = connect()
    success = True

    try:
        
        success &= delete_comment(id_ep=id)
        if not success:
            raise dataManipulationError('Failed to delete comment')

        sql = 'DELETE FROM episodes WHERE id = ?'
        cursor.execute(sql, (id,))

        conn.commit()
    except Exception as e:
        success = False
        print(e)
        conn.rollback()

    close(conn, cursor)
    return success

def delete_podcast(id):
    conn, cursor = connect()
    success = True

    try:

        # CASCADE
        episodes = get_episodes(id_podcast=id)
        for episode in episodes:
            id_ep = episode[0]
            success &= delete_episode(id_ep)        

        if not success:
            raise dataManipulationError('Failed to delete podcast')

        # ON DELETE
        sql = 'DELETE FROM podcasts WHERE id = ?'
        cursor.execute(sql, (id,))

        conn.commit()
    except Exception as e:
        success = False
        print(e)
        conn.rollback()

    close(conn, cursor)
    return success

# CONNECT AND CLOSE

def connect():
    conn = sqlite3.connect(PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    return conn, cursor

def close(conn, cursor):
    cursor.close()
    conn.close()