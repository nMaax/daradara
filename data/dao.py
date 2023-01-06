import sqlite3
import os

FILENAME = 'data.db'
SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))

PATH = os.path.join(SCRIPT_DIR, FILENAME)

# SELECT

def get_users():
    output = []
    for i in range(1, get_last_user_id()):
        output.append(get_user(id = i))
    return output

def get_user(id):
    conn, cursor = connect()
    user = False

    try:
        sql = 'SELECT * FROM users where id = ?'
        cursor.execute(sql, (id,))
        user = cursor.fetchone()
    except Exception as e:
        print(e)
        conn.rollback()

    close(conn, cursor)

    return user

def get_last_user_id():
    conn, cursor = connect()
    id = False

    try:
        sql = 'SELECT MAX(id) FROM users'
        cursor.execute(sql)
        id = cursor.fetchone()['MAX(id)']
    except Exception as e:
        print(e)
        conn.rollback()

    close(conn, cursor)

    return id

def get_podcasts():
    output = []
    for i in range(1, get_last_podcast_id()):
        output.append(get_podcast(id = i))
    return output

def get_podcast(id):
    conn, cursor = connect()
    user = False

    try:
        sql = 'SELECT * FROM podcasts where id = ?'
        cursor.execute(sql, (id,))
        user = cursor.fetchone()
    except Exception as e:
        print(e)
        conn.rollback()

    close(conn, cursor)

    return user

def get_last_podcast_id():
    conn, cursor = connect()
    id = False

    try:
        sql = 'SELECT MAX(id) FROM podcasts'
        cursor.execute(sql)
        id = cursor.fetchone()['MAX(id)']
    except Exception as e:
        print(e)
        conn.rollback()

    close(conn, cursor)

    return id

# INSERT

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

# CONNECT AND CLOSE

def connect():
    conn = sqlite3.connect(PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    return conn, cursor

def close(conn, cursor):
    cursor.close()
    conn.close()
