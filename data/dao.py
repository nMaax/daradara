import sqlite3
import os

FILENAME = 'data.db'
SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
PATH = os.path.join(SCRIPT_DIR, FILENAME)

# SELECT QUERIES

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
    episodes = False

    try:
        sql = 'SELECT * FROM episode WHERE id_podcast = ?'
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
        sql = 'SELECT * FROM episode WHERE id = ?'
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

def get_user_by_username(username):
    conn, cursor = connect()
    user = False

    try:
        sql = 'SELECT * FROM users WHERE username = ?'
        cursor.execute(sql, (username,))
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

def get_podcasts():
    output = []
    for i in range(1, get_last_podcast_id() + 1 ):
        output.append(get_podcast(id = i))
    return output

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

# INSERT QUERIES

def new_follow(id_user, id_podcast):
    conn, cursor = connect()
    success = False

    try:
        sql = 'INSERT INTO follows(id_user, id_podcast) VALUES (?, ?)'
        cursor.execute(sql, (id_user, id_podcast))
        conn.commit()
        success = True
    except Exception as e:
        print(e)
        conn.rollback()

    close(conn, cursor)
    return success

def new_save(id_user, id_ep):
    conn, cursor = connect()
    success = False

    try:
        sql = 'INSERT INTO saves(id_user, id_ep) VALUES (?, ?)'
        cursor.execute(sql, (id_user, id_ep))
        conn.commit()
        success = True
    except Exception as e:
        print(e)
        conn.rollback()

    close(conn, cursor)
    return success

def new_comment(id_user, id_ep, text, timestamp):
    conn, cursor = connect()
    success = False

    try:
        sql = 'INSERT INTO comments(id_user, id_ep, text, timestamp) VALUES (?, ?, ?, ?)'
        cursor.execute(sql, (id_user, id_ep, text, timestamp))
        conn.commit()
        success = True
    except Exception as e:
        print(e)
        conn.rollback()

    close(conn, cursor)
    return success

def new_episode(title, description, audio, timestamp, id_podcast):
    conn, cursor = connect()
    success = False

    try:
        sql = 'INSERT INTO episodes(title, description, audio, timestamp, id_podcast) VALUES (?, ?, ?, ?, ?)'
        cursor.execute(sql, (title, description, audio, timestamp, id_podcast))
        conn.commit()
        success = True
    except Exception as e:
        print(e)
        conn.rollback()

    close(conn, cursor)
    return success

def new_podcast(title, description, img, id_user, tags):
    conn, cursor = connect()
    success_pod, success_tag = False, False

    try:
        sql = 'INSERT INTO podcasts(title, desc, img, id_user) VALUES (?, ?, ?, ?)'
        cursor.execute(sql, (title, description, img, id_user))
        conn.commit()
        success_pod = True
    except Exception as e_pod:
        print(e_pod)
        conn.rollback()

    if success_pod:
        id_podcast = get_last_podcast_id()
        try:
            for tag in tags:
                sql = 'INSERT INTO categories(id_podcast, tag) VALUES (?, ?)'
                cursor.execute(sql, (id_podcast, tag))
                conn.commit()
                success_tag = True
        except Exception as e_tag:
            print(e_tag)
            conn.rollback()

    close(conn, cursor)
    return success_pod, success_tag

def new_user(username, email, password, name, surname, bio, propic):
    conn, cursor = connect()
    success = False

    try:
        sql = 'INSERT INTO users(username, email, password, name, surname, bio, propic) VALUES (?, ?, ?, ?, ?, ?, ?)'
        cursor.execute(sql, (username, email, password, name, surname, bio, propic))
        conn.commit()
        success = True
    except Exception as e:
        print(e)
        conn.rollback()

    close(conn, cursor)
    return success

# MODIFY QUERIES

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
    success = False

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
        success = True
    except Exception as e:
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
    success = False

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
        success = True
    except Exception as e:
        print(e)
        conn.rollback()

    close(conn, cursor)
    return success

# DELETE QUERIES
#TODO ON DELETE CASCADE

def delete_episode(id):
    conn, cursor = connect()
    success = False

    try:
        sql = 'DELETE FROM episodes WHERE id = ?'
        cursor.execute(sql, (id,))
        conn.commit()
        success = True
    except Exception as e:
        print(e)
        conn.rollback()

    close(conn, cursor)
    return success

def delete_podcast(id):
    conn, cursor = connect()
    success = False

    try:
        sql = 'DELETE FROM podcasts WHERE id = ?'
        cursor.execute(sql, (id,))
        conn.commit()
        success = True
    except Exception as e:
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