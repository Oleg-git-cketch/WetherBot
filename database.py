import sqlite3


connection = sqlite3.connect('delivery.db', check_same_thread=False)
sql = connection.cursor()

sql.execute('CREATE TABLE IF NOT EXISTS users (tg_id INTEGER PRIMARY KEY, name TEXT, number TEXT);')
sql.execute('CREATE TABLE IF NOT EXISTS location (latitude REAL, longitude REAL);')

def register(tg_id, name, number):
    sql.execute('INSERT INTO users (tg_id, name, number) VALUES (?, ?, ?);', (tg_id, name, number))
    connection.commit()

def location(latitude, longitude):
    sql.execute('INSERT INTO location VALUES (?, ?);', (latitude, longitude))
    connection.commit()

def check_user(tg_id):
    if sql.execute('SELECT * FROM users WHERE tg_id=?;', (tg_id,)).fetchone():
        return True
    else:
        return False
