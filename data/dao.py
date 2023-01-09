import sqlite3
import os
from data.errors.daoExceptions import dataManipulationError

FILENAME = 'data.db'
SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
PATH = os.path.join(SCRIPT_DIR, FILENAME)

# SELECT queries

def get_saves_join_episodes(id_user):
    conn, cursor = connect()
    saves = False

    try:
        sql = 'SELECT * FROM saves, episodes WHERE saves.id_ep = episodes.id AND id_user = ?'
        cursor.execute(sql, (id_user,))
        saves = cursor.fetchall()
    except Exception as e:
        print(e)

    close(conn, cursor)
    return saves

def get_saves(id_user):
    conn, cursor = connect()
    saves = False

    try:
        sql = 'SELECT * FROM saves WHERE id_user = ?'
        cursor.execute(sql, (id_user,))
        saves = cursor.fetchall()
    except Exception as e:
        print(e)

    close(conn, cursor)
    return saves

def get_follows_join_podcasts(id_user):
    conn, cursor = connect()
    follows = False

    try:
        # Nonostante non vi siano altre collonne che si chiamino 'id_user' COMUNQUE sqlite vuole che si tolga ambiguità con follows.id_user invece di id_user e basta, uffi :(
        sql = 'SELECT * FROM follows, podcasts WHERE follows.id_podcast = podcasts.id AND follows.id_user = ?'
        cursor.execute(sql, (id_user,))
        follows = cursor.fetchall()
    except Exception as e:
        print(e)

    close(conn, cursor)
    return follows

def get_follows(id_user):
    conn, cursor = connect()
    follows = False

    try:
        sql = 'SELECT * FROM follows WHERE id_user = ?'
        cursor.execute(sql, (id_user,))
        follows = cursor.fetchall()
    except Exception as e:
        print(e)

    close(conn, cursor)
    return follows

def get_tags(id_podcast):
    conn, cursor = connect()
    tags = False

    try:
        sql = 'SELECT * FROM categories WHERE id_podcast = ?'
        cursor.execute(sql, (id_podcast,))
        tags = cursor.fetchall()
    except Exception as e:
        print(e)

    close(conn, cursor)
    return tags

def get_comments(id_ep=None, id_user=None):
    conn, cursor = connect()
    comments = False
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

def get_comment(id):
    conn, cursor = connect()
    comment = False

    try:
        sql = 'SELECT * FROM comments WHERE id = ?'
        cursor.execute(sql, (id,))
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

def get_episode(id):
    conn, cursor = connect()
    episode = False

    try:
        sql = 'SELECT * FROM episodes WHERE id = ?'
        cursor.execute(sql, (id,))
        episode = cursor.fetchone()
    except Exception as e:
        print(e)

    close(conn, cursor)
    return episode

def get_users():
    output = []
    for i in range(1, get_last_id_user() + 1):
        output.append(get_user(id = i))
    return output

def get_user_by_email(email):
    conn, cursor = connect()
    user = False

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
    user = False

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
    id = False

    try:
        sql = 'SELECT MAX(id) FROM users'
        cursor.execute(sql)
        id = cursor.fetchone()['MAX(id)']
    except Exception as e:
        print(e)

    close(conn, cursor)    
    return id

def get_podcast_extended(id_podcast):
    conn, cursor = connect()
    podcast = False

    try:
        #['id', 'title', 'desc', 'img', 'id_user', 'id', 'email', 'password', 'name', 'surname', 'propic', 'id', 'title', 'description', 'audio', 'timestamp', 'id_podcast']
        sql = 'SELECT * FROM podcasts, users, episodes WHERE podcasts.id_user = users.id AND episodes.id_podcast = podcasts.id AND id_podcast = ? ORDER BY podcasts.id, episodes.id ASC'
        cursor.execute(sql, (id_podcast,))
        podcast = cursor.fetchall()
    except Exception as e:
        print(e)

    close(conn, cursor)
    return podcast

def get_podcasts_onfire(number_of_podcasts=5):
    conn, cursor = connect()
    podcast = []

    try:
        sql = "SELECT podcasts.id, COUNT(follows.id_user) AS 'n_follows', podcasts.title, podcasts.desc FROM podcasts, follows WHERE podcasts.id = follows.id_podcast GROUP BY podcasts.id ORDER BY n_follows DESC"
        cursor.execute(sql)
        podcast = cursor.fetchall()
    except Exception as e:
        print(e)

    close(conn, cursor)
    return podcast[:number_of_podcasts]

def get_podcasts():
    output = []
    for i in range(1, get_last_podcast_id() + 1 ):
        output.append(get_podcast(id = i))
    return output

def get_podcasts_by_user(id_user):
    conn, cursor = connect()
    #? Posso anche togliere il try e podcast = False?
    podcast = False

    try:
        sql = 'SELECT * FROM podcasts WHERE id_user = ?'
        cursor.execute(sql, (id_user,))
        podcast = cursor.fetchall()
    except Exception as e:
        print(e)

    close(conn, cursor)
    return podcast

def get_podcast(id):
    conn, cursor = connect()
    podcast = False

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
    id = False

    try:
        sql = 'SELECT MAX(id) FROM podcasts'
        cursor.execute(sql)
        id = cursor.fetchone()['MAX(id)']
    except Exception as e:
        print(e)

    close(conn, cursor)
    return id

# INSERT queries

def new_follow(id_user, id_podcast):
    conn, cursor = connect()
    success = True

    try:
        sql = 'INSERT INTO follows(id_user, id_podcast) VALUES (?, ?)'
        cursor.execute(sql, (id_user, id_podcast))
        conn.commit()
    except Exception as e:
        success = False
        print(e)
        conn.rollback()

    close(conn, cursor)
    return success

def new_save(id_user, id_ep):
    conn, cursor = connect()
    success = True

    try:
        sql = 'INSERT INTO saves(id_user, id_ep) VALUES (?, ?)'
        cursor.execute(sql, (id_user, id_ep))
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

def new_podcast(title, description, img, id_user, tags):
    conn, cursor = connect()
    success = True

    try:
        sql = 'INSERT INTO podcasts(title, desc, img, id_user) VALUES (?, ?, ?, ?)'
        cursor.execute(sql, (title, description, img, id_user))

        #! Rendi questo pezzo di codice più elegante
        id_podcast = get_last_podcast_id()
        if id_podcast:
            id_podcast += 1
        else:
            id_podcast = 1
        for tag in tags:
            sql = 'INSERT INTO categories(id_podcast, tag) VALUES (?, ?)'
            cursor.execute(sql, (id_podcast, tag))

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

def update_episode(id, title=None, desc=None, audio=None, timestamp=None):
    if title is not None:
        update_episode_field(id, 'title', title)
    if desc is not None:
        update_episode_field(id, 'description', desc)
    if audio is not None:
        update_episode_field(id, 'audio', audio)
    if timestamp is not None:
        update_episode_field(id, 'timestamp', timestamp)

def update_episode_field(id, field, value):
    conn, cursor = connect()
    success = True

    try:
        if field == "title":
            sql = 'UPDATE episodes SET title = ? WHERE id = ?'
        elif field == "description":
            sql = 'UPDATE episodes SET description = ? WHERE id = ?'
        elif field == "audio":
            sql = 'UPDATE episodes SET audio = ? WHERE id = ?'
        elif field == "timestamp":
            sql = 'UPDATE episodes SET timestamp = ? WHERE id = ?'
        else:
            raise ValueError("Invalid field name")

        cursor.execute(sql, (value, id))
        conn.commit()
    except Exception as e:
        success = False
        print(e)
        conn.rollback()

    close(conn, cursor)
    return success

def update_podcast(id, title=None, desc=None, img=None):
    if title is not None:
        update_podcast_field(id, 'title', title)
    if desc is not None:
        update_podcast_field(id, 'desc', desc)
    if img is not None:
        update_podcast_field(id, 'img', img)

def update_podcast_field(id, field, value):
    conn, cursor = connect()
    success = True

    try:
        if field == "title":
            sql = 'UPDATE podcasts SET title = ? WHERE id = ?'
        elif field == "desc":
            sql = 'UPDATE podcasts SET desc = ? WHERE id = ?'
        elif field == "img":
            sql = 'UPDATE podcasts SET img = ? WHERE id = ?'
        else:
            raise ValueError("Invalid field name")

        cursor.execute(sql, (value, id))
        conn.commit()
    except Exception as e:
        success = False
        print(e)
        conn.rollback()

    close(conn, cursor)
    return success

# DELETE queries
#TODO ON DELETE CASCADE

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
            raise dataManipulationError("Failed to delete ...")

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
            raise dataManipulationError("Failed to delete ...")

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